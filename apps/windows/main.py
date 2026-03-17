"""PySide6 Windows desktop app for Taiwan Stock Radar v1.7."""

from __future__ import annotations

import json
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

try:
    from PySide6.QtCore import QDate, QObject, Qt, QThread, Signal, Slot
    from PySide6.QtWidgets import (
        QApplication,
        QComboBox,
        QDateEdit,
        QFormLayout,
        QGridLayout,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QListWidget,
        QMainWindow,
        QMessageBox,
        QPlainTextEdit,
        QProgressBar,
        QPushButton,
        QSpinBox,
        QTableWidget,
        QTableWidgetItem,
        QTabWidget,
        QVBoxLayout,
        QWidget,
        QHeaderView,
    )
except ModuleNotFoundError as exc:  # pragma: no cover - import guard for non-desktop environments
    raise SystemExit(
        "PySide6 is required to run the Windows desktop app. Install requirements-desktop.txt first."
    ) from exc


def _resource_root() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(getattr(sys, "_MEIPASS"))
    return Path(__file__).resolve().parents[2]


def _output_root(resource_root: Path) -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return resource_root


RESOURCE_ROOT = _resource_root()
OUTPUT_ROOT = _output_root(RESOURCE_ROOT)
SRC_DIR = RESOURCE_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from taiwan_stock_radar.config import load_mapping
from taiwan_stock_radar.demo_premarket_data import DEMO_PREMARKET_PROFILES
from taiwan_stock_radar.workflows import (
    generate_daily_market_brief,
    generate_market_scan,
    generate_premarket_brief,
    generate_single_stock_committee_report,
    list_report_history,
)


SETTINGS = load_mapping(RESOURCE_ROOT / "config" / "settings.yaml")
UNIVERSE = load_mapping(RESOURCE_ROOT / "config" / "universe.yaml")


def _qdate_to_iso(widget: QDateEdit) -> str:
    return widget.date().toString("yyyy-MM-dd")


def _set_table_text(table: QTableWidget, row: int, column: int, value: Any) -> None:
    item = QTableWidgetItem(str(value))
    item.setFlags(item.flags() ^ Qt.ItemIsEditable)
    table.setItem(row, column, item)


def _read_output_preview(path: str | None) -> str:
    if not path:
        return ""
    file_path = Path(path)
    if not file_path.exists():
        return ""
    return file_path.read_text(encoding="utf-8")


def _latest_timestamp(paths: dict[str, str]) -> str:
    candidates = [Path(path) for path in paths.values()]
    if not candidates:
        return "尚未產出"
    latest = max(candidates, key=lambda item: item.stat().st_mtime)
    return datetime.fromtimestamp(latest.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")


class WorkflowWorker(QObject):
    finished = Signal(object)
    failed = Signal(str)

    def __init__(self, fn: Callable[..., dict[str, Any]], kwargs: dict[str, Any]) -> None:
        super().__init__()
        self.fn = fn
        self.kwargs = kwargs

    @Slot()
    def run(self) -> None:
        try:
            result = self.fn(**self.kwargs)
        except Exception as exc:  # pragma: no cover - UI surface
            detail = "".join(traceback.format_exception_only(type(exc), exc)).strip()
            self.failed.emit(detail)
            return
        self.finished.emit(result)


class BaseWorkflowTab(QWidget):
    def __init__(self, title: str, on_refresh_dashboard: Callable[[], None]) -> None:
        super().__init__()
        self.on_refresh_dashboard = on_refresh_dashboard
        self._threads: list[tuple[QThread, WorkflowWorker]] = []

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: 700;")
        self.status_label = QLabel("待命中")
        self.status_label.setStyleSheet("color: #4b5563;")
        self.progress = QProgressBar()
        self.progress.setRange(0, 1)
        self.progress.setValue(0)
        self.progress.hide()
        self.last_output_label = QLabel("最近輸出：尚未產出")
        self.last_output_label.setStyleSheet("color: #6b7280;")

    def _top_block(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress)
        layout.addWidget(self.last_output_label)
        return layout

    def start_task(
        self,
        fn: Callable[..., dict[str, Any]],
        kwargs: dict[str, Any],
        on_success: Callable[[dict[str, Any]], None],
    ) -> None:
        self.status_label.setText("執行中，請稍候...")
        self.progress.show()
        self.progress.setRange(0, 0)

        thread = QThread(self)
        worker = WorkflowWorker(fn, kwargs)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.failed.connect(thread.quit)
        worker.finished.connect(lambda result: self._handle_success(thread, worker, result, on_success))
        worker.failed.connect(lambda message: self._handle_failure(thread, worker, message))
        thread.finished.connect(thread.deleteLater)

        self._threads.append((thread, worker))
        thread.start()

    def _handle_success(
        self,
        thread: QThread,
        worker: WorkflowWorker,
        result: dict[str, Any],
        on_success: Callable[[dict[str, Any]], None],
    ) -> None:
        self.progress.hide()
        self.progress.setRange(0, 1)
        self.status_label.setText("執行完成")
        self.last_output_label.setText(f"最近輸出：{_latest_timestamp(result.get('latest_outputs', {}))}")
        on_success(result)
        self.on_refresh_dashboard()
        self._cleanup_thread(thread, worker)

    def _handle_failure(self, thread: QThread, worker: WorkflowWorker, message: str) -> None:
        self.progress.hide()
        self.progress.setRange(0, 1)
        self.status_label.setText("執行失敗")
        QMessageBox.critical(self, "Workflow Error", message)
        self._cleanup_thread(thread, worker)

    def _cleanup_thread(self, thread: QThread, worker: WorkflowWorker) -> None:
        self._threads = [(t, w) for t, w in self._threads if t is not thread and w is not worker]


class DashboardTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        project = SETTINGS.get("project", {})
        app = SETTINGS.get("app", {})

        layout = QVBoxLayout(self)
        title = QLabel(app.get("title", project.get("display_name", "Taiwan Stock Radar")))
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        subtitle = QLabel(app.get("subtitle", "Shared core for skill and Windows desktop."))
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #4b5563;")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        status_group = QGroupBox("系統狀態 / System Status")
        status_layout = QGridLayout(status_group)
        self.version_label = QLabel(project.get("plan_version", "v1.7"))
        self.resource_label = QLabel(str(RESOURCE_ROOT))
        self.output_label = QLabel(str(OUTPUT_ROOT / SETTINGS.get("paths", {}).get("output_dir", "output")))
        self.history_count_label = QLabel("0")
        self.mode_label = QLabel(project.get("mode", "dual_track"))
        status_layout.addWidget(QLabel("Version"), 0, 0)
        status_layout.addWidget(self.version_label, 0, 1)
        status_layout.addWidget(QLabel("Resource Root"), 1, 0)
        status_layout.addWidget(self.resource_label, 1, 1)
        status_layout.addWidget(QLabel("Output Root"), 2, 0)
        status_layout.addWidget(self.output_label, 2, 1)
        status_layout.addWidget(QLabel("History Count"), 3, 0)
        status_layout.addWidget(self.history_count_label, 3, 1)
        status_layout.addWidget(QLabel("Mode"), 4, 0)
        status_layout.addWidget(self.mode_label, 4, 1)
        layout.addWidget(status_group)

        self.history_list = QListWidget()
        self.history_list.setMinimumHeight(240)
        layout.addWidget(QLabel("最近輸出 / Recent Outputs"))
        layout.addWidget(self.history_list)

        self.settings_preview = QPlainTextEdit()
        self.settings_preview.setReadOnly(True)
        self.settings_preview.setPlainText(
            json.dumps(
                {
                    "version": project.get("plan_version", "v1.7"),
                    "daily_market_brief": SETTINGS.get("daily_market_brief", {}),
                    "premarket": SETTINGS.get("premarket", {}),
                    "scan": SETTINGS.get("scan", {}),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        self.settings_preview.setMinimumHeight(140)
        layout.addWidget(QLabel("設定摘要 / Settings Snapshot"))
        layout.addWidget(self.settings_preview)

        refresh_button = QPushButton("重新整理 Dashboard")
        refresh_button.clicked.connect(self.refresh)
        layout.addWidget(refresh_button, alignment=Qt.AlignLeft)
        layout.addStretch(1)
        self.refresh()

    def refresh(self) -> None:
        entries = list_report_history(RESOURCE_ROOT, output_root=OUTPUT_ROOT, limit=20)
        self.history_count_label.setText(str(len(entries)))
        self.history_list.clear()
        for item in entries:
            symbol = f" / {item['symbol']}" if item.get("symbol") else ""
            self.history_list.addItem(
                f"{item['analysis_date']} | {item['report_type']}{symbol} | {item['modified_at']}"
            )


class DailyBriefTab(BaseWorkflowTab):
    def __init__(self, on_refresh_dashboard: Callable[[], None]) -> None:
        super().__init__("08:30 日盤報告 / Daily Market Brief", on_refresh_dashboard)
        layout = QVBoxLayout(self)
        layout.addLayout(self._top_block())

        controls = QHBoxLayout()
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setCalendarPopup(True)
        run_button = QPushButton("執行 08:30 報告")
        run_button.clicked.connect(self.run_report)
        controls.addWidget(QLabel("分析日期"))
        controls.addWidget(self.date_edit)
        controls.addWidget(run_button)
        controls.addStretch(1)
        layout.addLayout(controls)

        self.summary_label = QLabel("等待產生報告。")
        self.summary_label.setWordWrap(True)
        layout.addWidget(self.summary_label)

        self.message_table = QTableWidget(0, 3)
        self.message_table.setHorizontalHeaderLabels(["來源", "區段", "訊息"])
        self.message_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.message_table.setMinimumHeight(220)
        layout.addWidget(self.message_table)

        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)
        layout.addWidget(self.preview, stretch=1)

    def run_report(self) -> None:
        self.start_task(
            generate_daily_market_brief,
            {
                "project_root": RESOURCE_ROOT,
                "analysis_date": _qdate_to_iso(self.date_edit),
                "output_root": OUTPUT_ROOT,
            },
            self._populate,
        )

    def _populate(self, bundle: dict[str, Any]) -> None:
        report = bundle["report"]
        self.summary_label.setText(
            f"{report['overall_label']} | 開盤 {report['opening_bias']} {report['opening_score']}/100 | "
            f"綜合 {report['overall_score']}/100"
        )
        self.message_table.setRowCount(len(report["top_messages"]))
        for row, item in enumerate(report["top_messages"]):
            _set_table_text(self.message_table, row, 0, item["source"])
            _set_table_text(self.message_table, row, 1, item["section"])
            _set_table_text(self.message_table, row, 2, item["title"])
        self.preview.setPlainText(_read_output_preview(bundle["latest_outputs"].get("md")))


class PremarketTab(BaseWorkflowTab):
    def __init__(self, on_refresh_dashboard: Callable[[], None]) -> None:
        super().__init__("開市前報告 / Premarket Brief", on_refresh_dashboard)
        layout = QVBoxLayout(self)
        layout.addLayout(self._top_block())

        controls = QHBoxLayout()
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setCalendarPopup(True)
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(sorted(DEMO_PREMARKET_PROFILES))
        run_button = QPushButton("執行開市前報告")
        run_button.clicked.connect(self.run_report)
        controls.addWidget(QLabel("分析日期"))
        controls.addWidget(self.date_edit)
        controls.addWidget(QLabel("Profile"))
        controls.addWidget(self.profile_combo)
        controls.addWidget(run_button)
        controls.addStretch(1)
        layout.addLayout(controls)

        self.summary_label = QLabel("等待產生報告。")
        self.summary_label.setWordWrap(True)
        layout.addWidget(self.summary_label)

        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)
        layout.addWidget(self.preview, stretch=1)

    def run_report(self) -> None:
        self.start_task(
            generate_premarket_brief,
            {
                "project_root": RESOURCE_ROOT,
                "analysis_date": _qdate_to_iso(self.date_edit),
                "profile": self.profile_combo.currentText(),
                "output_root": OUTPUT_ROOT,
            },
            self._populate,
        )

    def _populate(self, bundle: dict[str, Any]) -> None:
        report = bundle["report"]
        self.summary_label.setText(
            f"{report['opening_bias']} | 分數 {report['opening_score']}/100 | {report['expected_opening_plan']}"
        )
        self.preview.setPlainText(_read_output_preview(bundle["latest_outputs"].get("md")))


class ScanTab(BaseWorkflowTab):
    def __init__(self, on_refresh_dashboard: Callable[[], None]) -> None:
        super().__init__("Top20 掃描 / Market Scan", on_refresh_dashboard)
        layout = QVBoxLayout(self)
        layout.addLayout(self._top_block())

        controls = QHBoxLayout()
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setCalendarPopup(True)
        self.regime_combo = QComboBox()
        self.regime_combo.addItems(["bull", "sideways", "bear", "high_volatility"])
        self.top_n_spin = QSpinBox()
        self.top_n_spin.setRange(5, 50)
        self.top_n_spin.setValue(20)
        run_button = QPushButton("執行 Top20 掃描")
        run_button.clicked.connect(self.run_report)
        controls.addWidget(QLabel("分析日期"))
        controls.addWidget(self.date_edit)
        controls.addWidget(QLabel("Regime"))
        controls.addWidget(self.regime_combo)
        controls.addWidget(QLabel("Top N"))
        controls.addWidget(self.top_n_spin)
        controls.addWidget(run_button)
        controls.addStretch(1)
        layout.addLayout(controls)

        self.scan_table = QTableWidget(0, 7)
        self.scan_table.setHorizontalHeaderLabels(["Symbol", "Name", "Sector", "Score", "Direction", "Buy Zone", "Stop"])
        self.scan_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.scan_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.scan_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.scan_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.scan_table.setMinimumHeight(260)
        layout.addWidget(self.scan_table)

        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)
        layout.addWidget(self.preview, stretch=1)

    def run_report(self) -> None:
        self.start_task(
            generate_market_scan,
            {
                "project_root": RESOURCE_ROOT,
                "analysis_date": _qdate_to_iso(self.date_edit),
                "regime": self.regime_combo.currentText(),
                "top_n": self.top_n_spin.value(),
                "output_root": OUTPUT_ROOT,
            },
            self._populate,
        )

    def _populate(self, bundle: dict[str, Any]) -> None:
        report = bundle["report"]
        rows = report["top20"]
        self.scan_table.setRowCount(len(rows))
        for row_index, item in enumerate(rows):
            _set_table_text(self.scan_table, row_index, 0, item["symbol"])
            _set_table_text(self.scan_table, row_index, 1, item["name"])
            _set_table_text(self.scan_table, row_index, 2, item["sector"])
            _set_table_text(self.scan_table, row_index, 3, item["radar_score"])
            _set_table_text(self.scan_table, row_index, 4, item["direction_bias"])
            _set_table_text(self.scan_table, row_index, 5, item["buy_zone"])
            _set_table_text(self.scan_table, row_index, 6, item["stop_loss"])
        self.preview.setPlainText(_read_output_preview(bundle["latest_outputs"].get("md")))


class SingleStockTab(BaseWorkflowTab):
    def __init__(self, on_refresh_dashboard: Callable[[], None]) -> None:
        super().__init__("單股委員會 / Single-Stock Committee", on_refresh_dashboard)
        layout = QVBoxLayout(self)
        layout.addLayout(self._top_block())

        controls = QHBoxLayout()
        self.symbol_combo = QComboBox()
        for item in UNIVERSE.get("symbols", []):
            self.symbol_combo.addItem(f"{item['symbol']} {item['name']}", item["symbol"])
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setCalendarPopup(True)
        self.style_combo = QComboBox()
        self.style_combo.addItems(["short_term", "swing", "position"])
        run_button = QPushButton("執行單股委員會")
        run_button.clicked.connect(self.run_report)
        controls.addWidget(QLabel("股票"))
        controls.addWidget(self.symbol_combo)
        controls.addWidget(QLabel("分析日期"))
        controls.addWidget(self.date_edit)
        controls.addWidget(QLabel("Style"))
        controls.addWidget(self.style_combo)
        controls.addWidget(run_button)
        controls.addStretch(1)
        layout.addLayout(controls)

        summary_group = QGroupBox("Action Plan Snapshot")
        summary_form = QFormLayout(summary_group)
        self.thesis_label = QLabel("等待產生報告。")
        self.thesis_label.setWordWrap(True)
        self.buy_zone_label = QLabel("-")
        self.stop_label = QLabel("-")
        self.tp_label = QLabel("-")
        self.confidence_label = QLabel("-")
        summary_form.addRow("Final Thesis", self.thesis_label)
        summary_form.addRow("Buy Zone", self.buy_zone_label)
        summary_form.addRow("Stop Loss", self.stop_label)
        summary_form.addRow("Take Profit", self.tp_label)
        summary_form.addRow("Confidence", self.confidence_label)
        layout.addWidget(summary_group)

        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)
        layout.addWidget(self.preview, stretch=1)

    def run_report(self) -> None:
        self.start_task(
            generate_single_stock_committee_report,
            {
                "project_root": RESOURCE_ROOT,
                "symbol": self.symbol_combo.currentData(),
                "analysis_date": _qdate_to_iso(self.date_edit),
                "style": self.style_combo.currentText(),
                "output_root": OUTPUT_ROOT,
            },
            self._populate,
        )

    def _populate(self, bundle: dict[str, Any]) -> None:
        report = bundle["report"]
        self.thesis_label.setText(report["final_thesis"])
        self.buy_zone_label.setText(report["buy_zone"])
        self.stop_label.setText(report["stop_loss"])
        self.tp_label.setText(f"{report['take_profit_plan']['tp1']} / {report['take_profit_plan']['tp2']}")
        self.confidence_label.setText(f"{report['confidence']['label']} ({report['confidence']['score']}/100)")
        self.preview.setPlainText(_read_output_preview(bundle["latest_outputs"].get("md")))
        if "generated_daily_brief" in bundle:
            self.status_label.setText("執行完成，並已自動補產生日盤報告。")


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        project = SETTINGS.get("project", {})
        app = SETTINGS.get("app", {})
        self.setWindowTitle(
            f"{app.get('title', project.get('display_name', 'Taiwan Stock Radar'))} Desktop {project.get('plan_version', 'v1.7')}"
        )
        self.resize(1360, 920)

        tabs = QTabWidget()
        self.dashboard_tab = DashboardTab()
        self.daily_tab = DailyBriefTab(self.dashboard_tab.refresh)
        self.premarket_tab = PremarketTab(self.dashboard_tab.refresh)
        self.scan_tab = ScanTab(self.dashboard_tab.refresh)
        self.single_stock_tab = SingleStockTab(self.dashboard_tab.refresh)

        tabs.addTab(self.dashboard_tab, "Dashboard")
        tabs.addTab(self.daily_tab, "08:30 日盤報告")
        tabs.addTab(self.premarket_tab, "開市前報告")
        tabs.addTab(self.scan_tab, "Top20 掃描")
        tabs.addTab(self.single_stock_tab, "單股委員會")
        self.setCentralWidget(tabs)


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

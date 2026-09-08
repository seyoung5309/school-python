import sys
import json
import urllib.request
import urllib.error
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QPlainTextEdit,
    QLabel
)
from PySide6.QtCore import Qt, QThread, Signal

# Ollama API 호출을 담당하는 백그라운드 스레드
class OllamaWorker(QThread):
    finished_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self, error_text: str, model_name: str = "llama3"):
        super().__init__()
        self.error_text = error_text
        self.model_name = model_name

    def run(self):
        url = "http://localhost:11434/api/generate"
        prompt = (
            "당신은 친절한 파이썬 에러 튜터입니다. "
            "다음 파이썬 에러 메시지의 원인과 해결 방법을 고등학생 눈높이에 맞게 한국어로 쉽게 설명해 주세요.\n\n"
            f"[에러 메시지]\n{self.error_text}"
        )

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url, data=data, headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))
                ans = result.get("response", "답변을 가져오지 못했습니다.")
                self.finished_signal.emit(ans)
        except urllib.error.URLError:
            self.error_signal.emit(
                "[오류] Ollama 서버에 연결할 수 없습니다.\n"
                "1. Ollama가 실행 중인지 확인하세요 (ollama serve).\n"
                "2. terminal에서 'ollama run llama3' 명령어로 모델이 설치되어 있는지 확인하세요."
            )
        except Exception as e:
            self.error_signal.emit(f"[오류 발생] {str(e)}")


class TutorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("파이썬 에러 튜터")
        self.resize(550, 750)
        self.setMinimumSize(450, 600)

        self.worker = None
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # 1. 상단 섹션
        header_box = QVBoxLayout()
        header_box.setSpacing(4)

        title_label = QLabel("파이썬 에러 튜터")
        title_label.setObjectName("titleLabel")

        subtitle_label = QLabel("발생한 파이썬 에러 메시지를 아래에 붙여넣어 주세요.")
        subtitle_label.setObjectName("subtitleLabel")

        header_box.addWidget(title_label)
        header_box.addWidget(subtitle_label)
        main_layout.addLayout(header_box)

        # 2. 에러 입력 섹션
        input_box = QVBoxLayout()
        input_box.setSpacing(6)

        input_header = QLabel("에러 메시지 입력")
        input_header.setObjectName("sectionHeader")

        self.input_edit = QPlainTextEdit()
        self.input_edit.setPlaceholderText("예: SyntaxError: invalid syntax 또는 NameError: name 'x' is not defined...")
        self.input_edit.setObjectName("inputEdit")

        input_box.addWidget(input_header)
        input_box.addWidget(self.input_edit)

        main_layout.addLayout(input_box, stretch=2)

        # 3. 중앙 제어 섹션
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)

        self.analyze_btn = QPushButton("분석하기")
        self.analyze_btn.setObjectName("analyzeBtn")
        self.analyze_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.analyze_btn.clicked.connect(self.start_analysis)

        self.clear_btn = QPushButton("지우기")
        self.clear_btn.setObjectName("clearBtn")
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_all)

        self.status_label = QLabel("상태: 준비됨")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        control_layout.addWidget(self.analyze_btn, stretch=2)
        control_layout.addWidget(self.clear_btn, stretch=1)
        control_layout.addWidget(self.status_label, stretch=2)

        main_layout.addLayout(control_layout)

        # 4. 하단 결과 섹션
        output_box = QVBoxLayout()
        output_box.setSpacing(6)

        output_header = QLabel("분석 결과")
        output_header.setObjectName("sectionHeader")

        self.output_edit = QPlainTextEdit()
        self.output_edit.setReadOnly(True)
        self.output_edit.setPlaceholderText("분석 결과가 여기에 표시됩니다.")
        self.output_edit.setObjectName("outputEdit")

        output_box.addWidget(output_header)
        output_box.addWidget(self.output_edit)

        main_layout.addLayout(output_box, stretch=3)

        self.setCentralWidget(central_widget)

        # Tab 키 이동 순서
        QWidget.setTabOrder(self.input_edit, self.analyze_btn)
        QWidget.setTabOrder(self.analyze_btn, self.clear_btn)
        QWidget.setTabOrder(self.clear_btn, self.output_edit)

        self.apply_styles()

    def apply_styles(self):
        style_sheet = """
            QWidget {
                background-color: #f8fafc;
                color: #1e293b;
                font-family: 'Malgun Gothic', 'Pretendard', 'Segoe UI', sans-serif;
                font-size: 16px;
            }
            #titleLabel {
                font-size: 22px;
                font-weight: bold;
                color: #0f172a;
            }
            #subtitleLabel {
                font-size: 14px;
                color: #64748b;
                margin-bottom: 4px;
            }
            #sectionHeader {
                font-size: 16px;
                font-weight: bold;
                color: #334155;
            }
            QPlainTextEdit {
                background-color: #ffffff;
                color: #0f172a;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
            }
            QPlainTextEdit:focus {
                border: 2px solid #10b981;
            }
            QPlainTextEdit:disabled {
                background-color: #f1f5f9;
                color: #94a3b8;
                border: 1px solid #e2e8f0;
            }
            #outputEdit {
                background-color: #f1f5f9;
                border: 1px solid #cbd5e1;
            }
            #analyzeBtn {
                background-color: #10b981;
                color: #ffffff;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-size: 16px;
            }
            #analyzeBtn:hover {
                background-color: #059669;
            }
            #analyzeBtn:disabled {
                background-color: #cbd5e1;
                color: #94a3b8;
            }
            #clearBtn {
                background-color: #e2e8f0;
                color: #334155;
                font-weight: bold;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 10px 16px;
                font-size: 16px;
            }
            #clearBtn:hover {
                background-color: #cbd5e1;
            }
            #clearBtn:disabled {
                background-color: #f1f5f9;
                color: #cbd5e1;
                border: 1px solid #e2e8f0;
            }
            #statusLabel {
                font-weight: bold;
                color: #0284c7;
                background-color: #e0f2fe;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 15px;
            }
        """
        self.setStyleSheet(style_sheet)

    def start_analysis(self):
        text = self.input_edit.toPlainText().strip()

        if not text:
            self.status_label.setText("에러 내용을 입력해주세요")
            self.status_label.setStyleSheet(
                "font-weight: bold; color: #dc2626; background-color: #fee2e2; border-radius: 8px; padding: 8px 12px; font-size: 15px;"
            )
            return

        self.status_label.setText("상태: 분석 중...")
        self.status_label.setStyleSheet(
            "font-weight: bold; color: #d97706; background-color: #fef3c7; border-radius: 8px; padding: 8px 12px; font-size: 15px;"
        )

        self.input_edit.setEnabled(False)
        self.analyze_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)

        # Ollama 호출 백그라운드 스레드 생성 (모델명을 본인 환경에 맞춰 변경 가능, 예: 'qwen2.5', 'llama3')
        self.worker = OllamaWorker(error_text=text, model_name="llama3")
        self.worker.finished_signal.connect(self.on_analysis_success)
        self.worker.error_signal.connect(self.on_analysis_error)
        self.worker.start()

    def on_analysis_success(self, response_text):
        self.output_edit.setPlainText(response_text)
        self.status_label.setText("상태: 완료")
        self.status_label.setStyleSheet(
            "font-weight: bold; color: #16a34a; background-color: #dcfce7; border-radius: 8px; padding: 8px 12px; font-size: 15px;"
        )
        self.reset_controls()

    def on_analysis_error(self, error_message):
        self.output_edit.setPlainText(error_message)
        self.status_label.setText("상태: 오류 발생")
        self.status_label.setStyleSheet(
            "font-weight: bold; color: #dc2626; background-color: #fee2e2; border-radius: 8px; padding: 8px 12px; font-size: 15px;"
        )
        self.reset_controls()

    def reset_controls(self):
        self.input_edit.setEnabled(True)
        self.analyze_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)

    def clear_all(self):
        self.input_edit.clear()
        self.output_edit.clear()
        self.status_label.setText("상태: 준비됨")
        self.status_label.setStyleSheet(
            "font-weight: bold; color: #0284c7; background-color: #e0f2fe; border-radius: 8px; padding: 8px 12px; font-size: 15px;"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TutorApp()
    window.show()
    sys.exit(app.exec())
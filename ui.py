import sys
import yaml
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QComboBox, QLineEdit, QLabel, \
    QVBoxLayout, QHBoxLayout, QWidget


class BaseUI:
    def __init__(self, ui):
        self.ui = ui
        self.is_editable = False
        self.controls = {}

    # 添加一个输入框
    def add_input(self, form_layout, key, label):
        item = {
            # 容器控件
            'layout': QHBoxLayout(),
            # label控件
            'label': QLabel(label, self.ui),
            # 编辑框控件，例如输入框、下拉框等
            'edit': QLineEdit(self.ui),
            # 值回显控件
            'text': QLabel(self.ui),
            # 值
            'value': '',
            # key
            'key': '',
            'type': 'QLineEdit',
        }
        # 然后根据判断，看 form_layout 放哪个
        item['layout'].addWidget(item['label'])
        item['layout'].addWidget(item['edit'])
        item['layout'].addWidget(item['text'])

        if self.is_editable:
            item['text'].hide()
        else:
            item['edit'].hide()

        form_layout.addLayout(item['layout'])
        self.controls[key] = item
        return item

    # 添加一个下拉框
    def add_select(self, form_layout, key, label, options):
        item = {
            # 容器控件
            'layout': QHBoxLayout(),
            # label控件
            'label': QLabel(label, self.ui),
            # 编辑框控件，例如输入框、下拉框等
            'edit': QComboBox(self.ui),
            # 值回显控件
            'text': QLabel(self.ui),
            # 值
            'value': '',
            # key
            'key': '',
            'type': 'QComboBox',
        }
        # 然后根据判断，看 form_layout 放哪个
        item['layout'].addWidget(item['label'])

        for option in options:
            item['edit'].addItem(option['label'], option['value'])

        item['layout'].addWidget(item['edit'])
        item['layout'].addWidget(item['text'])

        if self.is_editable:
            print('text 隐藏')
            item['text'].hide()
        else:
            print('edit 隐藏')
            item['edit'].hide()

        form_layout.addLayout(item['layout'])
        self.controls[key] = item
        return item

    def edit_enable(self):
        self.is_editable = True
        self.update_controls()

    def edit_disable(self):
        self.is_editable = False
        self.update_controls()

    def update_controls(self):
        for key in self.controls:
            if self.is_editable is True:
                self.controls[key]['text'].hide()
                self.controls[key]['edit'].show()
            else:
                self.controls[key]['text'].show()
                self.controls[key]['edit'].hide()

    def get_value(self):

        m = {}
        for key in self.controls:
            if self.controls[key]['type'] == 'QLineEdit':
                # 单行输入框
                m[key] = self.controls[key]['edit'].text()
            elif self.controls[key]['type'] == 'QTextEdit':
                # 多行输入框
                m[key] = self.controls[key]['edit'].toPlainText()
            elif self.controls[key]['type'] == 'QSpinBox' or self.controls[key]['type'] == 'QDoubleSpinBox':
                # 用于整数和浮点数输入
                m[key] = self.controls[key]['edit'].value()
            elif self.controls[key]['type'] == 'QCheckBox':
                # 复选框
                m[key] = self.controls[key]['edit'].isChecked()
            elif self.controls[key]['type'] == 'QRadioButton':
                # 单选按钮
                m[key] = self.controls[key]['edit'].isChecked()
            elif self.controls[key]['type'] == 'QComboBox':
                # 下拉框
                m[key] = self.controls[key]['edit'].currentText()
            elif self.controls[key]['type'] == 'QSlider':
                # 滑块
                m[key] = self.controls[key]['edit'].value()
            elif self.controls[key]['type'] == 'QDateEdit':
                # 日期选择器
                m[key] = self.controls[key]['edit'].date()
            elif self.controls[key]['type'] == 'QDateTimeEdit':
                # 日期时间选择器
                m[key] = self.controls[key]['edit'].dateTime()

        return m

    def set_value(self, data):
        for key in data:
            if key in self.controls:
                if self.controls[key]['type'] == 'QLineEdit':
                    # 单行输入框
                    self.controls[key]['edit'].setText(data[key])
                elif self.controls[key]['type'] == 'QTextEdit':
                    # 多行输入框
                    self.controls[key]['edit'].setPlainText(data[key])
                elif self.controls[key]['type'] == 'QSpinBox' or self.controls[key]['type'] == 'QDoubleSpinBox':
                    # 用于整数和浮点数输入
                    self.controls[key]['edit'].setValue(data[key])
                elif self.controls[key]['type'] == 'QCheckBox':
                    # 复选框
                    self.controls[key]['edit'].setChecked(data[key])
                elif self.controls[key]['type'] == 'QRadioButton':
                    # 单选按钮
                    self.controls[key]['edit'].setChecked(data[key])
                elif self.controls[key]['type'] == 'QComboBox':
                    # 下拉框
                    self.controls[key]['edit'].setCurrentText(data[key])
                elif self.controls[key]['type'] == 'QSlider':
                    # 滑块
                    self.controls[key]['edit'].setValue(data[key])
                elif self.controls[key]['type'] == 'QDateEdit':
                    # 日期选择器
                    self.controls[key]['edit'].setDate(data[key])
                elif self.controls[key]['type'] == 'QDateTimeEdit':
                    # 日期时间选择器
                    self.controls[key]['edit'].setDateTime(data[key])
                self.controls[key]['text'].setText(data[key])


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button_print = None
        self.button_edit_enable = None
        self.button_edit_disable = None
        self.main_widget = None
        self.main_layout = None
        self.form_widget = None
        self.form_layout = None

        self.modelSelect = None
        self.token = None
        self.form_list = []
        self.baseUI = BaseUI(self)
        self.initUI()

    def initUI(self):
        # 创建表单布局
        self.form_layout = QVBoxLayout()

        # 查询模式
        self.modelSelect = self.baseUI.add_select(self.form_layout, 'model', '查询模式', [
            {"label": "群组group", "value": "group"},
            {"label": "单项目repository", "value": "repository"},
            {"label": "多项目repositories", "value": "repositories"},
        ])

        # 访问令牌
        self.token = self.baseUI.add_input(self.form_layout, 'gitlab_api_access_token', '个人访问令牌')

        # # 创建编辑和保存按钮
        self.button_print = QPushButton('打印值', self)
        self.button_print.clicked.connect(self.log)
        self.button_edit_enable = QPushButton('编辑', self)
        self.button_edit_enable.clicked.connect(self.set_status_edit)
        self.button_edit_disable = QPushButton('保存', self)
        self.button_edit_disable.clicked.connect(self.save_data)
        # 创建表单
        self.form_widget = QWidget(self)
        self.form_widget.setLayout(self.form_layout)

        # 创建主布局
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.form_widget)
        # 添加按钮
        self.main_layout.addWidget(self.button_print)
        self.main_layout.addWidget(self.button_edit_enable)
        self.main_layout.addWidget(self.button_edit_disable)

        self.main_widget = QWidget(self)
        self.main_widget.setLayout(self.main_layout)

        # 设置窗口大小和标题
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('示例程序')
        self.setCentralWidget(self.main_widget)
        self.show()

    def log(self):
        print(self.baseUI.get_value())

    def set_status_edit(self):
        self.baseUI.edit_enable()
        self.button_edit_enable.hide()
        self.button_edit_disable.show()

    def set_status_text(self):
        self.baseUI.edit_disable()
        self.button_edit_enable.show()
        self.button_edit_disable.hide()

    def save_data(self):
        data = self.baseUI.get_value()
        self.baseUI.set_value(data)
        self.set_status_text()

    def set_value(self, data):
        self.baseUI.set_value(data)

    def loadYaml(self, fileName):
        # 从yml文件中加载数据，并将其显示在表单中
        with open(fileName, 'r') as f:
            data = yaml.safe_load(f)
        self.nameEdit.setText(data.get('姓名', ''))
        gender = data.get('性别', '')
        if gender in ['男', '女']:
            self.genderCombo.setCurrentText(gender)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    ex.set_status_text()
    # 加载yml文件
    # ex.loadYaml('test.yml')
    sys.exit(app.exec_())

import sys
import yaml
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QComboBox, QLineEdit, QLabel, \
    QVBoxLayout, QHBoxLayout, QWidget, QFormLayout, QSizePolicy
from PyQt5.QtCore import Qt


class BaseUI:
    def __init__(self, ui):
        self.ui = ui
        self.is_editable = False
        self.controls = {}
        self.label_width = 120
        self.row_height = 20

    # 添加一个输入框
    def add_input(self, form_layout, key, label, callback=lambda text: text):
        item = {
            # 容器控件
            'layout': QWidget(),
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
        layout = QHBoxLayout()
        item['layout'].setLayout(layout)

        # 设定 item['label'] 的宽度
        item['label'].setFixedWidth(self.label_width)
        item['label'].setFixedHeight(self.row_height)
        item['edit'].setFixedHeight(self.row_height)
        item['text'].setFixedHeight(self.row_height)
        item['edit'].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        item['text'].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        item['edit'].textChanged.connect(callback)
        # 然后根据判断，看 form_layout 放哪个
        layout.addWidget(item['label'], 1, alignment=Qt.AlignLeft)
        layout.addWidget(item['edit'], 10, alignment=Qt.AlignLeft)
        layout.addWidget(item['text'], 10, alignment=Qt.AlignLeft)

        if self.is_editable:
            item['text'].hide()
        else:
            item['edit'].hide()

        form_layout.addRow(item['layout'])
        self.controls[key] = item
        return item

    # 添加一个下拉框
    def add_select(self, form_layout, key, label, options, callback=lambda text: text):
        # 嵌套关系
        # - form_layout                     QFormLayout 表单控件
        #   - item['layout']                QWidget     本行最外围的空间
        #     - layout                      QHBoxLayout
        #       - item['label']             QLabel      文字
        #       - right_widget              QWidget
        #         - right_widget_layout     QHBoxLayout
        #           - item['edit']          QComboBox   编辑输入框
        #           - item['text']          QLabel      纯文本显示值
        item = {
            # 容器控件
            'layout': QWidget(),
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
        #
        layout = QHBoxLayout(item['layout'])
        layout.setContentsMargins(20, 0, 20, 0)
        layout.addWidget(item['label'])
        item['l'] = layout

        # 生成一个右侧的widget，将编辑/文本两个控件填充进去
        right_widget = QWidget()

        # 生成 right_widget 的子容器，将其填充进去
        right_widget_layout = QHBoxLayout(right_widget)
        right_widget_layout.setContentsMargins(0, 0, 0, 0)
        right_widget_layout.addWidget(item['edit'])
        right_widget_layout.addWidget(item['text'])
        # 设置最里面的2个的宽度
        item['edit'].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        item['text'].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout.addWidget(right_widget)

        # 设定 item['label'] 的宽度
        item['label'].setFixedWidth(self.label_width)
        item['label'].setFixedHeight(self.row_height)
        item['edit'].setFixedHeight(self.row_height)
        item['text'].setFixedHeight(self.row_height)

        # 然后根据判断，看 form_layout 放哪个
        layout.addWidget(item['label'])

        for option in options:
            item['edit'].addItem(option['label'], option['value'])

        item['edit'].currentTextChanged.connect(lambda _: callback(item['edit'].currentData()))
        layout.addWidget(item['edit'])
        layout.addWidget(item['text'])

        if self.is_editable:
            item['text'].hide()
        else:
            item['edit'].hide()

        form_layout.addRow(item['layout'])
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
                m[key] = self.controls[key]['edit'].currentData()
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
        print('set_value', data)
        for key in data:
            if key in self.controls:
                if self.controls[key]['type'] == 'QLineEdit':
                    # 单行输入框
                    self.controls[key]['edit'].setText(data[key])
                    self.controls[key]['text'].setText(data[key])
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
                    index = self.controls[key]['edit'].findData(data[key])
                    if index != -1:
                        self.controls[key]['edit'].setCurrentIndex(index)
                        label = self.controls[key]['edit'].itemText(index)
                        self.controls[key]['text'].setText(label)
                    else:
                        print(f"key={key}，未找到对应的下拉框选项值：{data[key]}")
                elif self.controls[key]['type'] == 'QSlider':
                    # 滑块
                    self.controls[key]['edit'].setValue(data[key])
                elif self.controls[key]['type'] == 'QDateEdit':
                    # 日期选择器
                    self.controls[key]['edit'].setDate(data[key])
                elif self.controls[key]['type'] == 'QDateTimeEdit':
                    # 日期时间选择器
                    self.controls[key]['edit'].setDateTime(data[key])


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.test_only_show_branch = None
        self.test_mode = None
        self.file_search_engine = None
        self.gitlab_api_url = None
        self.string_to_search = None
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
        self.form_layout = QFormLayout()
        self.form_layout.setLabelAlignment(Qt.AlignLeft)
        self.form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.form_layout.setHorizontalSpacing(20)

        # 查询模式
        self.modelSelect = self.baseUI.add_select(self.form_layout, 'model', '查询模式', [
            {"label": "群组group", "value": "group"},
            {"label": "单项目repository", "value": "repository"},
            {"label": "多项目repositories", "value": "repositories"},
        ])

        # 访问令牌
        self.token = self.baseUI.add_input(self.form_layout, 'gitlab_api_access_token', '个人访问令牌')
        # 被搜索的字符串（限单行）
        self.string_to_search = self.baseUI.add_input(self.form_layout, 'string_to_search', '被搜索的字符串')
        # gitlab的地址
        self.gitlab_api_url = self.baseUI.add_input(self.form_layout, 'gitlab_api_url', 'gitlab地址')
        # 文件查询引擎
        self.file_search_engine = self.baseUI.add_select(self.form_layout, 'file_search_engine', '文件查询引擎', [
            {"label": "python", "value": "python"},
            {"label": "go", "value": "go"},
        ])

        # 测试模式
        self.test_mode = self.baseUI.add_select(self.form_layout, 'test_mode', '测试模式', [
            {"label": "开", "value": True},
            {"label": "关", "value": False},
        ], self.on_test_mode_change)
        # 测试模式
        self.test_only_show_branch = self.baseUI.add_select(self.form_layout, 'test_only_show_branch',
                                                            '只打印待处理的项目和分支', [
                                                                {"label": "开", "value": True},
                                                                {"label": "关", "value": False},
                                                            ])

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
        print("——————————————————————————")
        print('log', self.baseUI.get_value())
        print(self.form_layout.minimumSize())
        print(self.baseUI.controls['test_mode']['layout'].width())
        print(self.baseUI.controls['test_mode']['l'].minimumSize())
        print(self.baseUI.controls['test_mode']['edit'].width())

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

    def on_test_mode_change(self, value):
        print(value)
        if value is True:
            self.test_only_show_branch['layout'].show()
        else:
            self.test_only_show_branch['layout'].hide()

    def loadYaml(self, fileName):
        # 从yml文件中加载数据，并将其显示在表单中
        with open(fileName, 'r') as f:
            data = yaml.safe_load(f)

        self.baseUI.set_value(data)
        self.on_test_mode_change(data['test_mode'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    ex.set_status_text()
    # 加载yml文件
    ex.loadYaml('config_private.yml_bak')
    sys.exit(app.exec_())

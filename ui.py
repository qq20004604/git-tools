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
            'key': ''
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
            'key': ''
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

    def editEnable(self):
        self.is_editable = True
        self.update_controls()

    def editDisable(self):
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

        # new_controls = []
        # for label, control, control_type, *extra in self.controls:
        #     control.deleteLater()
        #
        #     if self.is_editable:
        #         if control_type == 'input':
        #             new_control = QLineEdit(self.ui)
        #             new_control.setText(control.text())
        #         elif control_type == 'select':
        #             options = extra[0]
        #             new_control = QComboBox(self.ui)
        #             for option in options:
        #                 new_control.addItem(option['label'], option['value'])
        #             new_control.setCurrentText(control.text())
        #     else:
        #         new_control = QLabel(self.ui)
        #         if control_type == 'input':
        #             new_control.setText(control.text())
        #         else:  # control_type == 'select'
        #             new_control.setText(control.currentText())
        #
        #     new_controls.append((label, new_control, control_type, *extra))
        #
        #     layout = control.parent()
        #     layout.addWidget(new_control)
        #
        # self.controls = new_controls


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
        self.button_edit_enable.clicked.connect(self.baseUI.editEnable)
        self.button_edit_disable = QPushButton('取消编辑', self)
        self.button_edit_disable.clicked.connect(self.baseUI.editDisable)
        # self.saveButton = QPushButton('保存', self)
        # self.saveButton.clicked.connect(self.save)
        # self.saveButton.hide()

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
        print(1)
        print(self.modelSelect.currentData())
        print(self.token.text())

    def edit(self):
        self.ui.editEnable()
        # # 将表单切换到编辑模式，并显示保存和取消按钮
        # self.modelSelect.setEnabled(True)
        # self.token.setReadOnly(False)
        # self.nameEdit.setReadOnly(False)
        # self.genderCombo.setEnabled(True)
        # self.editButton.hide()
        # self.saveButton.show()

    def save(self):
        pass
        # # 将表单切换到只读模式，并将表单数据保存到yml文件
        # self.nameEdit.setReadOnly(True)
        # self.genderCombo.setEnabled(False)
        # self.saveButton.hide()
        # self.editButton.show()
        # data = {'姓名': self.nameEdit.text(), '性别': self.genderCombo.currentText()}
        # fileName, _ = QFileDialog.getSaveFileName(self, '保存文件', '', 'YAML 文件 (*.yml)')
        # if fileName:
        #     with open(fileName, 'w') as f:
        #         yaml.safe_dump(data, f)

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
    # 加载yml文件
    # ex.loadYaml('test.yml')
    sys.exit(app.exec_())

#coding:utf-8
from __future__ import print_function, division
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle

from pic_process.char_recog import get_string_by_img
from pic_process.img_process import get_org_image, remove_noise, text_extract, line_extract, \
    char_extract, resize_img
from ui.base_ui.window_main_ui import  Ui_Window_Main as main_window
import sys
import os
import numpy as np
import scipy.ndimage as ndi
from skimage import measure,color

OPEN_FILE_NAME = "open_file_name"
DPI = 100
RISZIE_RATIO = 400
SELECTED_COLOR = "green"
DEFAULT_COLOR = "red"

class Main_windows(QMainWindow, main_window):
    # region 一些需要存储的变量的定义
    # 记录所处的阶段 0.刚读入图像 1.预处理阶段 2.行切分阶段 3.字符处理阶段 4.字符处理阶段
    processing_stage = 0
    # 该对象用于保存处理过程中各种中间图像 按下关闭文件按钮这个对象清空
    img_dic = {}
    # 用于存储当前画布中的图像的值
    show_img = None
    # 用于存储当前正在处理中的图像
    processing_img = None
    # 存储已经分为行的图片
    text_line_imgs = None
    # 最初的文本行信息
    text_line_position_array_org = None
    # 用于存储文本行文本行
    text_line_position_array = None
    # 文本行分割时候的行间留白 单位px
    text_line_margin = 50
    # 用于存储切分后的字符数组的位置，和text_line_image里面的image对应
    char_position_arr = None
    #
    layout_contents_top_margions = 10
    # axe_size
    axe_size = [0.0025, 0.0025, 0.995, 0.995]
    # char_rectangle 字符框的patch
    char_rectangle_patch = None
    # 识别的字符 label_list
    label_lists = []
    # 选中的文本行 用于对文本行的删除以及合并
    selected_text_line_index_list = []
    # 选中的字符 用于对字符进行合并，切分，删除等操作
    selected_char_index_list = []

    # endregion
    def __init__(self, parent=None):
        super(Main_windows, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("process")
        self.main_widget = QWidget(self)
        self.scroll = QScrollArea(self.main_widget)
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.scroll)
        self.main_widget.setLayout(layout)


        #事件处理

        # 文件 menu
        # 打开文件按钮
        self.action_open.triggered.connect(self.action_open_file_triggered)
        # 关闭文件按钮
        self.action_close.triggered.connect(self.action_close_file_triggered)
        # 退出
        self.action_exit.triggered.connect(lambda: sys.exit(0))

        # 预处理 menu
        # 去除噪点
        self.action_remove_noise.triggered.connect(self.action_remove_noise_triggered)
        # 倾斜矫正
        # self.action_tilt_correction.triggered.connect(self.action_tilt_correction_triggered)
        # 检测文字区域
        self.action_text_extract.triggered.connect(self.action_text_extract_triggered)

        #连通区域分析
        self.action_get_connect.triggered.connect(self.action_get_connect_triggered)

        self.setCentralWidget(self.main_widget)

    # region function: 绘制 current_img 图像中的值
    def show_image_on_widget(self):
        show_img = self.show_img
        if not (show_img is None):
            main_widget = QWidget()
            main_layout = QVBoxLayout()
            if len(show_img.shape) == 3:
                rows, cols, channels = show_img.shape
            elif len(show_img.shape) == 2:
                rows, cols = show_img.shape
            figsize = cols / DPI, rows / DPI
            fig = plt.figure(figsize=figsize)
            self.ax = fig.add_axes(self.axe_size)
            self.ax.spines['left'].set_color('none')
            self.ax.spines['right'].set_color('none')
            self.ax.spines['bottom'].set_color('none')
            self.ax.spines['top'].set_color('none')
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.ax.imshow(show_img, cmap="gray")
            self.canvas = FigureCanvas(fig)
            self.canvas.draw()
            self.show_img = show_img
            main_layout.addWidget(self.canvas)
            main_widget.setLayout(main_layout)
            self.scroll.setWidget(main_widget)
            plt.close()
        else:
            self.scroll.setWidget(QWidget())

    # endregion

    # region function: 绘制 行 将切分好的行图像拼接成 一张图像并展示文字区域
    def show_mutil_images_on_widget2(self):
        if self.text_line_imgs is None:
            self.scroll.setWidget(QWidget())
        else:
            main_widget = QWidget()
            main_layout = QVBoxLayout()
            # 生成需要展示的图像并更新行的位置
            rows, cols = self.processing_img.shape
            new_line_postion = []
            img = np.ones((self.text_line_margin, cols))
            row_count = img.shape[0]
            for i, line_img in enumerate(self.text_line_imgs):
                line_img_rows, line_img_cols = line_img.shape
                line_img_tmp = np.ones((line_img_rows, cols))
                line_img_tmp[:line_img_rows, :line_img_cols] = line_img
                img = np.vstack([img, line_img_tmp, np.ones((self.text_line_margin, cols))])
                self.text_line_imgs[i] = line_img_tmp
                new_line_postion.append((
                    row_count,
                    row_count + line_img_rows,
                    0,
                    cols))
                row_count += line_img.shape[0] + self.text_line_margin
            rows = img.shape[0]
            figsize = cols / RISZIE_RATIO, rows / RISZIE_RATIO
            fig = plt.figure(figsize=figsize)
            # print(figsize)
            self.ax = fig.add_axes(self.axe_size)
            self.ax.spines['left'].set_color('none')
            self.ax.spines['right'].set_color('none')
            self.ax.spines['bottom'].set_color('none')
            self.ax.spines['top'].set_color('none')
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.ax.imshow(img, cmap='gray')
            for i, line_position in enumerate(new_line_postion):
                min_row, max_row, min_col, max_col = line_position
                rec = Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, fill=False, ec="red",
                                picker=True)
                rec.line_index = i
                self.ax.add_patch(rec)
            self.canvas = FigureCanvas(fig)
            self.canvas.draw()
            self.canvas.mpl_connect('pick_event', self.on_line_pick)
            self.processing_img = img
            self.text_line_position_array = new_line_postion
            self.selected_text_line_index_list = []
            main_layout.addWidget(self.canvas)
            main_widget.setLayout(main_layout)
            self.scroll.setWidget(main_widget)

    # endregion

    # region  function: 绘制 字符 已经切分的字符数组
    def show_char_image_on_widget(self):

        if self.char_position_arr is None:
            return
        else:
            main_widget = QWidget()
            main_layout = QVBoxLayout()
            rows, cols = self.processing_img.shape
            figsize = cols / RISZIE_RATIO, rows / RISZIE_RATIO
            fig = plt.figure(figsize=figsize)
            self.ax = fig.add_axes(self.axe_size)
            self.ax.spines['left'].set_color('white')
            self.ax.spines['right'].set_color('white')
            self.ax.spines['bottom'].set_color('white')
            self.ax.spines['top'].set_color('white')
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.ax.imshow(self.processing_img, cmap='gray')
            self.char_rectangle_patch = []
            for line_index, (line_char_postion, line_position) in enumerate(
                    zip(self.char_position_arr, self.text_line_position_array)):
                line_start_row, _, line_start_col, _ = line_position
                line_patch = []
                for char_index, char_position in enumerate(line_char_postion):
                    char_start_row, char_end_row, char_start_col, char_end_col = char_position
                    rect_x = char_start_col
                    rect_y = line_start_row + char_start_row
                    rect_width = char_end_col - char_start_col
                    rect_height = char_end_row - char_start_row
                    char_rect = Rectangle((rect_x, rect_y), rect_width, rect_height, fill=False, edgecolor="red",
                                          picker=True)
                    # 保存 char_rect 的 index
                    char_rect.char_index = [line_index, char_index]
                    line_patch.append(char_rect)
                    self.ax.add_patch(char_rect)
                self.char_rectangle_patch.append(line_patch)

            self.canvas = FigureCanvas(fig)
            self.canvas.mpl_connect('pick_event', self.on_char_pick)
            self.canvas.draw()
            main_layout.addWidget(self.canvas)
            main_widget.setLayout(main_layout)
            self.scroll.setWidget(main_widget)
            plt.close()
            self.selected_char_index_list = []

    # endregion

    # region function: 打开文件
    def action_open_file_triggered(self):
        file_name_tuple = QFileDialog.getOpenFileName(self, "打开文件", ".", "图片文件 (*.jpg *.png)")
        file_name, file_name_filter = file_name_tuple

        if len(file_name) == 0:
            print("未选择任何文件")
        else:
            self.img_dic[OPEN_FILE_NAME] = file_name
            self.processing_img, self.show_img = get_org_image(file_name)
            self.show_image_on_widget()

    # endregion

    # region function: 关闭文件
    def action_close_file_triggered(self):
        self.show_img = None
        self.processing_img = None
        self.show_image_on_widget()

    # endregion

    # region function: 噪点去除
    def action_remove_noise_triggered(self):
        if self.show_img is None:
            return
        img = remove_noise(self.processing_img)
        self.show_img = resize_img(img)
        self.processing_img = img
        self.show_image_on_widget()

    # endregion

    # region function: 倾斜矫正
    # def action_tilt_correction_triggered(self):
    #     if self.show_img is None:
    #         return
    #     img = tilt_correction(self.processing_img)
    #     self.show_img = resize_img(img)
    #     self.processing_img = img
    #     self.show_image_on_widget()
    # endregion

    # region function: 文字区域检测
    def action_text_extract_triggered(self):
        if self.show_img is None:
            return
        img = text_extract(self.processing_img)
        self.show_img = resize_img(img)
        self.processing_img = img
        self.show_image_on_widget()
        self.processing_stage = 1

        # endregion

    def action_get_connect_triggered(self):
        if self.show_img is None:
            print("error")
            return
        labels = measure.label(self.show_img, connectivity=2)
        dst = color.label2rgb(labels)
        self.show_img = dst
        self.show_image_on_widget()
        print(len(labels))

from openvino.inference_engine import IECore, IENetwork
import cv2
import numpy as np
import time


# 使用方法：创建实例对象
# begin = Start()
# begin.path = 图片路径
# begin.run()
class Refctor():
    def __init__(self, path):
        self.path = path

    def save_output(sefl, res, ih, iw):
        # res = self.normPRED(res)
        res = res.squeeze()
        res = res * 255
        res = cv2.resize(res, (iw, ih))
        # im = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        return res

    def pre_process(self, path):
        img = cv2.imread(path, 0)
        img = img[:, :, np.newaxis]
        ih, iw = img.shape[:2]
        temp_img = np.zeros((img.shape[0], img.shape[1], 1))
        temp_img[:, :] = (img[:, :] - 0.306) / 0.4
        h, w = ih, iw
        if ih > 1300 or iw > 1300:
            r = iw / ih
            h = 1080
            w = int(h * r)
            temp_img = cv2.resize(temp_img, (w, h))
            temp_img = temp_img[:, :, np.newaxis]
        temp_img = temp_img.transpose((2, 0, 1))
        temp_img = temp_img[np.newaxis, :, :, :]
        return temp_img, ih, iw, h, w

    def run(self, net, ie):
        start = time.clock()
        start1 = start
        input_blob = next(iter(net.input_info))
        out_blob = next(iter(net.outputs))
        image, ih, iw, h, w = self.pre_process(self.path)
        net.reshape({input_blob: (1, 1, h, w)})
        exec_net = ie.load_network(network=net, device_name='CPU')
        res = exec_net.infer(inputs={input_blob: image})
        start = time.clock()
        res = res[out_blob]
        result = self.save_output(res, ih, iw)
        result = result.astype(np.uint8)
        # 二值化
        ret, thresh = cv2.threshold(result, 127, 255, cv2.THRESH_BINARY)
        # 寻找轮廓
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        a = thresh.shape[0] * thresh.shape[1] * 0.002
        thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

        img_contours = []
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i], False)
            if area < a:
                cv2.drawContours(thresh, contours, i, (0, 0, 0), -1)
        return result


class Start():
    def __init__(self):
        # 原图路径
        self.path = ""
        # 原图名字
        self.image_name = ""
        # mask保存的文件夹
        self.mask_path = "gui_utils/mask/"
        # mat保存的文件夹
        self.mat_path = "gui_utils/mat/"
        # mask的完整路径
        self.mask_total_path = ""
        # mat的完整路径
        self.mat_total_path = ""
        # 运行时间
        self.time_run = 0
        # 加载模型
        self.ie = IECore()
        self.net = self.ie.read_network("model/u2P_edge.xml", "model/u2P_edge.bin")
        self.exec_net = self.ie.load_network(network=self.net, device_name='CPU')
        self.srnet = self.ie.read_network("model/srcnn3x.xml", "model/srcnn3x.bin")

    def output_foreground(self, threshod=128):
        """
        根据原图和mask提取出主题，并生成透明背景
        Args:
            img: 抠图图像路径
            threshod: 像素渐变处的阈值
        """
        # 读取img和mask图片
        self.mat_total_path = self.mat_path + "mat_" + self.image_name + ".png"
        img = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), -1)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        img = img / max(img)
        mask = cv2.imread(self.mask_total_path)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGBA)
        a = mask[:, :, 3]
        r = mask[:, :, 0]
        a[r < threshod] = 0
        img[:, :, 3] = a
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        cv2.imwrite(self.mat_total_path, img)
        print("[INFO] " + self.mat_total_path + " save successful!")

    def normPRED(self, img):
        "归一化输出的mask,是ndarry数组"
        ma = img.max()
        mi = img.min()
        img = (img - mi) / (ma - mi)
        return img

    def pre_process2image(self, image_path, output_size=320):
        img = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), -1)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        ih, iw = img.shape[:2]
        image = img / np.max(img)
        image = cv2.resize(image, (320, 320))
        tmpImg = np.zeros((image.shape[0], image.shape[1], 3))
        # temp = np.max(img)
        if image.shape[2] == 1:
            tmpImg[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
            tmpImg[:, :, 1] = (image[:, :, 0] - 0.485) / 0.229
            tmpImg[:, :, 2] = (image[:, :, 0] - 0.485) / 0.229
        else:
            tmpImg[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
            tmpImg[:, :, 1] = (image[:, :, 1] - 0.456) / 0.224
            tmpImg[:, :, 2] = (image[:, :, 2] - 0.406) / 0.225
        tmpImg = tmpImg.transpose((2, 0, 1))
        print("[INFO] preprocess finished!")
        return tmpImg, ih, iw

    def output_mask(self, res, iw, ih, start):
        res = self.normPRED(res)
        res = res.squeeze()
        res = res * 255
        # im = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        imo = cv2.resize(res, (iw, ih))
        self.mask_total_path = self.mask_path + "mask_" + self.image_name + ".png"
        cv2.imwrite(self.mask_total_path, imo)
        redo = Refctor(self.mask_total_path)
        imo = redo.run(self.srnet, self.ie)
        print(f"infer work has used the time about {time.clock() - start}s")
        start = time.clock()
        cv2.imwrite(self.mask_total_path, imo)
        return start

    def run(self):
        # 设置好图片和路径
        print("[INFO]load the information in input")
        img_path = self.path
        temp = self.path.split("/")[-1]
        self.image_name = temp.split(".")[0]
        start = time.clock()
        start1 = time.clock()
        # 获取输入，输出层的名称
        print("[INFO] get information about the network of input and output")
        input_blob = next(iter(self.net.input_info))
        out_blob = next(iter(self.net.outputs))
        # 读取应该输入的数据
        # 对图片进行预处理，并输出原图尺寸
        image, ih, iw = self.pre_process2image(img_path)
        print("[INFO] preprocess finish")
        print("[INFO] Preprocess work has used the time about " + str(time.clock() - start) + " seconds")
        start = time.clock()
        # 开始推理

        print("[INFO] begin to infer the input")
        res = self.exec_net.infer(inputs={input_blob: image})

        # 结果处理
        print("[INFO] handle the result of infer")
        res = res[out_blob]
        # 输出mask
        start = self.output_mask(res, iw, ih, start)
        # print("[INFO] Infer work has used the time about " + str(time.clock() - start) + " seconds")
        start = time.clock()
        # 输出前景
        self.output_foreground()
        print("[INFO] last work has used the time about " + str(time.clock() - start) + " seconds")
        end = time.clock()
        self.time_run = end - start1
        print("[INFO] This work has used the time about " + str(end - start1) + " seconds")


if __name__ == '__main__':
    a = Start()
    a.path = r"F:\datasets\None classified based fronting obj segmentation datasets for A02\TESTING\17.jpg"
    a.run()

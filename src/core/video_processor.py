"""
视频处理核心模块
负责视频解码、编码和各种基本变换操作
"""

import os
import cv2
import numpy as np
import time


class VideoProcessor:
    """视频处理器类，提供视频处理的基础功能"""
    
    def __init__(self, input_path, output_dir="output"):
        """
        初始化视频处理器
        
        Args:
            input_path: 输入视频文件路径
            output_dir: 输出目录
        """
        self.input_path = input_path
        self.output_dir = output_dir
        self.cap = None
        self.frames = []
        self.fps = 0
        self.width = 0
        self.height = 0
        
    def load_video(self):
        """加载视频文件并获取基本信息"""
        self.cap = cv2.VideoCapture(self.input_path)
        if not self.cap.isOpened():
            print(f"无法打开视频文件: {self.input_path}")
            return False
        
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"视频已加载: {self.width}x{self.height}, {self.fps}fps")
        return True
    
    def extract_frames(self, max_frames=None):
        """提取视频帧
        
        Args:
            max_frames: 最大提取帧数，None表示提取全部
        """
        if not self.cap or not self.cap.isOpened():
            print("视频未加载")
            return False
        
        count = 0
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            self.frames.append(frame)
            count += 1
            
            if max_frames and count >= max_frames:
                break
        
        print(f"提取了 {len(self.frames)} 帧")
        return True
    
    def process_frames(self, operation="resize", params=None):
        """处理视频帧
        
        Args:
            operation: 操作类型，支持 resize, gray, blur
            params: 操作参数
        """
        if not self.frames:
            print("没有可处理的帧")
            return False
            
        processed_frames = []
        
        for frame in self.frames:
            if operation == "resize":
                scale = params.get("scale", 0.5) if params else 0.5
                new_width = int(self.width * scale)
                new_height = int(self.height * scale)
                processed_frame = cv2.resize(frame, (new_width, new_height))
                
            elif operation == "gray":
                processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # 转回3通道以便保存
                processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)
                
            elif operation == "blur":
                ksize = params.get("ksize", 5) if params else 5
                processed_frame = cv2.GaussianBlur(frame, (ksize, ksize), 0)
                
            else:
                processed_frame = frame.copy()
                
            processed_frames.append(processed_frame)
        
        self.frames = processed_frames
        print(f"已处理 {len(self.frames)} 帧，操作: {operation}")
        return True
    
    def save_video(self, output_filename="processed.mp4"):
        """保存处理后的视频
        
        Args:
            output_filename: 输出文件名
        """
        if not self.frames:
            print("没有帧可保存")
            return False
            
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        output_path = os.path.join(self.output_dir, output_filename)
        
        # 定义编码器和创建VideoWriter对象
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, self.fps, 
                             (self.frames[0].shape[1], self.frames[0].shape[0]))
        
        for frame in self.frames:
            out.write(frame)
            
        out.release()
        print(f"视频已保存至: {output_path}")
        return True
    
    def close(self):
        """释放资源"""
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.frames = []
        print("资源已释放")
        
    def __del__(self):
        """析构函数"""
        self.close()


def batch_process_videos(input_dir, output_dir, operation="resize", params=None):
    """批量处理视频文件
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        operation: 处理操作
        params: 操作参数
    """
    if not os.path.exists(input_dir):
        print(f"输入目录不存在: {input_dir}")
        return False
        
    video_extensions = [".mp4", ".avi", ".mov", ".mkv"]
    video_files = []
    
    for filename in os.listdir(input_dir):
        if any(filename.endswith(ext) for ext in video_extensions):
            video_files.append(os.path.join(input_dir, filename))
    
    print(f"找到 {len(video_files)} 个视频文件")
    
    for video_file in video_files:
        filename = os.path.basename(video_file)
        output_filename = f"processed_{filename}"
        
        processor = VideoProcessor(video_file, output_dir)
        if not processor.load_video():
            continue
            
        processor.extract_frames()
        processor.process_frames(operation, params)
        processor.save_video(output_filename)
        processor.close()
        
    return True


if __name__ == "__main__":
    # 示例用法
    video_processor = VideoProcessor("input.mp4")
    if video_processor.load_video():
        video_processor.extract_frames()
        video_processor.process_frames("resize", {"scale": 0.75})
        video_processor.save_video()
        video_processor.close()

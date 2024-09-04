import os
from PIL import Image


def compress_image(input_file_path, output_file_path, max_size_kb, initial_quality=95, quality_step=5,
                   resolution_step=0.9):
    # 打开图像文件
    with Image.open(input_file_path) as img:
        initial_size = os.path.getsize(input_file_path) / 1024
        quality = initial_quality
        width, height = img.size

        # 优先降低图像质量
        while initial_size > max_size_kb and quality > 10:
            img.save(output_file_path, optimize=True, quality=quality)
            initial_size = os.path.getsize(output_file_path) / 1024
            quality -= quality_step

        # 如果质量降低不足以达到目标大小，则降低分辨率
        while initial_size > max_size_kb:
            width = int(width * resolution_step)
            height = int(height * resolution_step)
            img = img.resize((width, height), Image.LANCZOS)
            img.save(output_file_path, optimize=True, quality=quality)
            initial_size = os.path.getsize(output_file_path) / 1024


def process_folder(input_folder, output_folder, max_size_kb, initial_quality=95, quality_step=5, resolution_step=0.9):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 统计文件总数
    total_files = sum([len(files) for _, _, files in os.walk(input_folder)])
    current_file_index = 0

    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            input_file_path = os.path.join(root, filename)
            # 在输出文件夹中保留相同的目录结构
            relative_path = os.path.relpath(root, input_folder)
            output_sub_folder = os.path.join(output_folder, relative_path)
            if not os.path.exists(output_sub_folder):
                os.makedirs(output_sub_folder)
            output_file_path = os.path.join(output_sub_folder, filename)

            if os.path.isfile(input_file_path):
                current_file_index += 1
                compress_image(input_file_path, output_file_path, max_size_kb, initial_quality, quality_step,
                               resolution_step)
                percentage = (current_file_index / total_files) * 100
                print(
                    f"Compressed {filename} to {output_file_path} ({current_file_index}/{total_files}, {percentage:.2f}%)")


if __name__ == "__main__":
    input_folder = input("Enter the input folder path: ")
    parent_folder, folder_name = os.path.split(input_folder.rstrip("/\\"))
    output_folder = os.path.join(parent_folder, f"{folder_name}_压缩")
    max_size_kb = int(input("Enter the max size in KB (e.g., 100): "))

    process_folder(input_folder, output_folder, max_size_kb)

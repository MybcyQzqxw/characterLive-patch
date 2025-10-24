"""
文件清理工具 - 可视化UI应用
用于删除指定项目中包含特定歌名的文件
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import json
import os
import sys
from pathlib import Path
import threading


class FileCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件清理工具")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # 默认路径配置
        self.default_paths = {
            'characterlive_path': r'E:\mine\gitspace\characterLive',
            'singsong_path': r'C:\MiaoMiao\singsong',
            'sovits_path': r'C:\MiaoMiao\so-vits-svc'
        }
        
        # 配置文件路径
        self.config_file = self.get_config_path()
        
        # 加载配置
        self.config = self.load_config()
        
        # 创建UI
        self.create_widgets()
        
        # 加载保存的路径（如果没有配置则使用默认值）
        self.load_saved_paths()
    
    def get_config_path(self):
        """获取配置文件路径"""
        if getattr(sys, 'frozen', False):
            # 打包后的exe，配置文件放在exe同目录
            app_dir = os.path.dirname(sys.executable)
        else:
            # 开发环境，配置文件放在脚本同目录
            app_dir = os.path.dirname(os.path.abspath(__file__))
        
        return os.path.join(app_dir, "config.json")
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.log_message(f"加载配置文件失败: {e}")
                return {}
        return {}
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            self.log_message("配置已保存")
        except Exception as e:
            self.log_message(f"保存配置失败: {e}")
    
    def create_widgets(self):
        """创建UI组件"""
        # 设置样式
        padding = {'padx': 10, 'pady': 5}
        
        # 第一行：characterLive项目地址
        row1_frame = tk.Frame(self.root)
        row1_frame.pack(fill=tk.X, **padding)
        
        tk.Label(row1_frame, text="characterLive项目:", width=18, anchor='w').pack(side=tk.LEFT)
        self.characterlive_entry = tk.Entry(row1_frame)
        self.characterlive_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        tk.Button(row1_frame, text="选择文件夹", command=lambda: self.browse_folder(self.characterlive_entry)).pack(side=tk.LEFT)
        
        # 第二行：singsong项目地址
        row2_frame = tk.Frame(self.root)
        row2_frame.pack(fill=tk.X, **padding)
        
        tk.Label(row2_frame, text="singsong项目:", width=18, anchor='w').pack(side=tk.LEFT)
        self.singsong_entry = tk.Entry(row2_frame)
        self.singsong_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        tk.Button(row2_frame, text="选择文件夹", command=lambda: self.browse_folder(self.singsong_entry)).pack(side=tk.LEFT)
        
        # 第三行：so-vits-svc项目地址
        row3_frame = tk.Frame(self.root)
        row3_frame.pack(fill=tk.X, **padding)
        
        tk.Label(row3_frame, text="so-vits-svc项目:", width=18, anchor='w').pack(side=tk.LEFT)
        self.sovits_entry = tk.Entry(row3_frame)
        self.sovits_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        tk.Button(row3_frame, text="选择文件夹", command=lambda: self.browse_folder(self.sovits_entry)).pack(side=tk.LEFT)
        
        # 第四行：歌名输入
        row4_frame = tk.Frame(self.root)
        row4_frame.pack(fill=tk.X, **padding)
        
        tk.Label(row4_frame, text="歌名:", width=18, anchor='w').pack(side=tk.LEFT)
        self.songname_entry = tk.Entry(row4_frame)
        self.songname_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.delete_button = tk.Button(row4_frame, text="删除", command=self.on_delete_click, bg='#ff6b6b', fg='white', font=('Arial', 10, 'bold'))
        self.delete_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 第五行：终端输出区域
        output_frame = tk.Frame(self.root)
        output_frame.pack(fill=tk.BOTH, expand=True, **padding)
        
        tk.Label(output_frame, text="输出信息:", anchor='w').pack(fill=tk.X)
        
        # 创建带滚动条的文本框
        self.output_text = scrolledtext.ScrolledText(
            output_frame, 
            wrap=tk.WORD, 
            height=15,
            state='disabled',
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='white',
            font=('Consolas', 9)
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # 欢迎信息
        self.log_message("=" * 80)
        self.log_message("欢迎使用文件清理工具！")
        self.log_message("请选择项目路径并输入要删除的歌名")
        self.log_message("=" * 80)
    
    def browse_folder(self, entry_widget):
        """浏览文件夹"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, folder_path)
    
    def load_saved_paths(self):
        """加载保存的路径，如果没有配置则使用默认值"""
        # characterLive 项目路径
        path = self.config.get('characterlive_path', self.default_paths['characterlive_path'])
        self.characterlive_entry.insert(0, path)
        
        # singsong 项目路径
        path = self.config.get('singsong_path', self.default_paths['singsong_path'])
        self.singsong_entry.insert(0, path)
        
        # so-vits-svc 项目路径
        path = self.config.get('sovits_path', self.default_paths['sovits_path'])
        self.sovits_entry.insert(0, path)
    
    def log_message(self, message):
        """在终端输出区域显示消息"""
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, message + '\n')
        self.output_text.see(tk.END)
        self.output_text.config(state='disabled')
        self.root.update_idletasks()
    
    def on_delete_click(self):
        """删除按钮点击事件"""
        # 获取输入值
        characterlive_path = self.characterlive_entry.get().strip()
        singsong_path = self.singsong_entry.get().strip()
        sovits_path = self.sovits_entry.get().strip()
        song_name = self.songname_entry.get().strip()
        
        # 验证输入
        if not song_name:
            messagebox.showwarning("警告", "请输入歌名！")
            return
        
        if not characterlive_path or not singsong_path or not sovits_path:
            messagebox.showwarning("警告", "请选择所有项目路径！")
            return
        
        # 保存配置
        self.config['characterlive_path'] = characterlive_path
        self.config['singsong_path'] = singsong_path
        self.config['sovits_path'] = sovits_path
        self.save_config()
        
        # 确认删除
        response = messagebox.askyesno(
            "确认删除", 
            f"确定要删除所有包含 '{song_name}' 的文件吗？\n\n此操作不可撤销！"
        )
        
        if not response:
            self.log_message("用户取消了删除操作")
            return
        
        # 禁用删除按钮，防止重复点击
        self.delete_button.config(state='disabled')
        
        # 在新线程中执行删除操作
        thread = threading.Thread(target=self.delete_files, args=(characterlive_path, singsong_path, sovits_path, song_name))
        thread.daemon = True
        thread.start()
    
    def delete_files(self, characterlive_path, singsong_path, sovits_path, song_name):
        """删除包含指定歌名的文件"""
        try:
            self.log_message("\n" + "=" * 80)
            self.log_message(f"开始搜索包含 '{song_name}' 的文件...")
            self.log_message("=" * 80)
            
            # 定义要搜索的目录列表
            search_dirs = []
            
            # characterLive/songs
            cl_songs = os.path.join(characterlive_path, "songs")
            if os.path.exists(cl_songs):
                search_dirs.append(("characterLive/songs", cl_songs))
            else:
                self.log_message(f"⚠ 警告: {cl_songs} 不存在")
            
            # singsong/songs
            ss_songs = os.path.join(singsong_path, "songs")
            if os.path.exists(ss_songs):
                search_dirs.append(("singsong/songs", ss_songs))
            else:
                self.log_message(f"⚠ 警告: {ss_songs} 不存在")
            
            # singsong/output
            ss_output = os.path.join(singsong_path, "output")
            if os.path.exists(ss_output):
                search_dirs.append(("singsong/output", ss_output))
            else:
                self.log_message(f"⚠ 警告: {ss_output} 不存在")
            
            # 统计信息
            total_found = 0
            total_deleted = 0
            total_failed = 0
            
            # 遍历每个目录
            for dir_name, dir_path in search_dirs:
                self.log_message(f"\n📁 正在搜索: {dir_name}")
                self.log_message(f"   路径: {dir_path}")
                
                found_files = []
                
                # 递归搜索文件
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        if song_name in file:
                            file_path = os.path.join(root, file)
                            found_files.append(file_path)
                
                if found_files:
                    self.log_message(f"   找到 {len(found_files)} 个文件:")
                    
                    for file_path in found_files:
                        total_found += 1
                        relative_path = os.path.relpath(file_path, dir_path)
                        self.log_message(f"   - {relative_path}")
                        
                        # 尝试删除文件
                        try:
                            os.remove(file_path)
                            total_deleted += 1
                            self.log_message(f"     ✓ 已删除")
                        except Exception as e:
                            total_failed += 1
                            self.log_message(f"     ✗ 删除失败: {e}")
                else:
                    self.log_message(f"   未找到包含 '{song_name}' 的文件")
            
            # 输出统计结果
            self.log_message("\n" + "=" * 80)
            self.log_message("删除操作完成！")
            self.log_message(f"找到文件: {total_found} 个")
            self.log_message(f"成功删除: {total_deleted} 个")
            if total_failed > 0:
                self.log_message(f"删除失败: {total_failed} 个")
            self.log_message("=" * 80)
            
        except Exception as e:
            self.log_message(f"\n❌ 错误: {e}")
            messagebox.showerror("错误", f"操作失败: {e}")
        finally:
            # 重新启用删除按钮
            self.root.after(0, lambda: self.delete_button.config(state='normal'))


def main():
    root = tk.Tk()
    app = FileCleanerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

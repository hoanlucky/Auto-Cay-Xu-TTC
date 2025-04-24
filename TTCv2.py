import re
import os
import time
import random
import requests
import threading
import webbrowser
import subprocess
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options




checkScam = requests.get("https://handtrickes.com/Tools/TTCv1.txt", proxies = None)
if "yes" in checkScam.text.lower():
	pass
else:
	def show_popup(r):
		popup = tk.Toplevel()
		popup.title("Thông báo")
		popup.geometry("400x200")
		tk.Label(popup, text="Tool chưa được kích hoạt", fg="blue", font=("Arial", 12, "bold")).pack(pady=10)
		tk.Label(popup, text="Vui lòng liên hệ nhà phát hành để kích hoạt\n\nWebsite: HandTrickes.com\nZalo: 0369723106", fg="black", font=("Arial", 12)).pack(pady=10)
		tk.Button(popup, text="Đã hiểu", command=r.destroy, font=("Arial", 12)).pack(pady=5)
		popup.protocol("WM_DELETE_WINDOW", root.destroy)
	root = tk.Tk()
	root.withdraw()
	show_popup(root)
	root.mainloop()
	quit()


def tao_trinh_duyet():
	list_trinh_duyet = []
	so_luong = int(re.sub(r'\D', '', so_luong_entry.get()) or "1")
	for luong in range(1, so_luong+1):
		options = webdriver.ChromeOptions()
		options.add_argument(f'--user-data-dir=/DataTrinhDuyet/ID{luong}')
		options.add_argument("--no-sandbox")
		options.add_argument("--disable-gpu")
		options.add_experimental_option("mobileEmulation", {
			"deviceName": "iPhone XR"
		})
		options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1")
		options.add_argument("--disable-blink-features=AutomationControlled")
		options.add_experimental_option("excludeSwitches", ["enable-automation"])
		options.add_experimental_option("useAutomationExtension", False)
		service = Service(r'chromedriver.exe')
		service.creationflags = subprocess.CREATE_NO_WINDOW
		driver = webdriver.Chrome(service=service,options=options)
		driver.set_window_size(414, 1000)
		driver.implicitly_wait(10)
		driver.get("https://m.youtube.com/results?search_query=hoanlucky+tool")
		time.sleep(5)
		list_trinh_duyet.append(driver)
	return list_trinh_duyet


def get_redirect_link(url):
	startupinfo = subprocess.STARTUPINFO()
	startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	result = subprocess.run(
		["curl", "-I", "-L", url], capture_output=True, text=True, startupinfo=startupinfo
	)
	redirect_links = [
		line.split(": ", 1)[1] for line in result.stdout.split("\n") if line.startswith("Location:")
	]
	if redirect_links:
		print("🔗 URL chuyển hướng:", redirect_links[-1])
		return redirect_links[-1]
	else:
		return False
		print("❌ Không tìm thấy URL chuyển hướng!")



def nhiem_vu_like_vip(max_nv_setting, driver_):
	driver = driver_
	driver.get("https://tuongtaccheo.com/kiemtien/likepostvipcheo/")
	time.sleep(7)
	dspost = driver.find_element("id", "dspost").find_elements("tag name", "div")
	max_nv = len(dspost)
	if max_nv > max_nv_setting:
		max_nv = max_nv_setting
	for x in range(1,max_nv+1):
		result = ""
		btn = driver.find_element("xpath", f"/html/body/div/div/div[2]/div/div[1]/div/div[{x}]/div/div/button")
		result = btn.get_attribute("title")
		id_nv_ttc = btn.get_attribute("onclick").split("'")[1]
		url_redirect = get_redirect_link(result.replace("'", ""))
		driver.execute_script(f"like('{id_nv_ttc}', '{url_redirect}')")
		tabs = driver.window_handles
		# Chuyển qua auto fb
		driver.switch_to.window(tabs[1])
		if "about:" in driver.current_url:
			driver.get(url_redirect)
		time.sleep(random.randint(1, 3))
		try:
			like_button = driver.find_element("xpath", "//div[@role='button' and (contains(@aria-label, 'like') or contains(@aria-label, 'thích'))]")
			driver.execute_script("arguments[0].click();", like_button)
		except:
			pass
		# Hết auto fb
		time.sleep(1.5)
		driver.close()
		driver.switch_to.window(tabs[0])
		time.sleep(1)
		driver.execute_script(f"nhantien('{id_nv_ttc}')")
		dem_lap = 0
		while True:
			if dem_lap == 10:
				return 0
				break
			try:
				alert = driver.find_element("xpath", "/html/body/div[2]/div/div").text
				result = f"[LIKE VIP CHEO] | {alert} | {result}\n"
				with open("History.txt", "a", encoding="utf-8") as file:
					file.write(result)
				if "thành công" in alert.lower():
					label2.config(text=f"{alert}", fg="green")
				else:
					label2.config(text=f"{alert}", fg="red")
				print(alert)
				break
			except:
				time.sleep(1)
				dem_lap = dem_lap + 1
		time.sleep(2)


def nhiem_vu_like_page(max_nv_setting, driver_):
	driver = driver_
	driver.get("https://tuongtaccheo.com/kiemtien/likepagecheo/")
	time.sleep(7)
	dspost = driver.find_element("id", "dspost").find_elements("tag name", "div")
	max_nv = len(dspost)
	if max_nv > max_nv_setting:
		max_nv = max_nv_setting
	for x in range(1,max_nv+1):
		result = ""
		btn = driver.find_element("xpath", f"/html/body/div/div/div[3]/div/div[1]/div/div[{x}]/div/div/button")
		result = btn.get_attribute("title")
		id_nv_ttc = btn.get_attribute("onclick").split("'")[1]
		url_redirect = result.replace("'", "")
		driver.execute_script(f"like('{id_nv_ttc}', '{url_redirect}')")
		tabs = driver.window_handles
		# Chuyển qua auto fb
		driver.switch_to.window(tabs[1])
		if "about:" in driver.current_url:
			driver.get(url_redirect)
		time.sleep(random.randint(5, 25))
		try:
			like_page_buttons = driver.find_element("xpath", "//div[@role='button' and (contains(@aria-label, 'Thích') or contains(@aria-label, 'Like'))]")
			if like_page_buttons:
				if any(item in url_redirect for item in ["photo", "videos", "posts", "watch", "permalink", "reel"]):
					pass
				else:
					driver.execute_script("arguments[0].click();", like_page_buttons)
					time.sleep(3)
			else:
				print("Không tìm thấy nút Like Page")
		except:
			pass
		# Hết auto fb
		driver.close()
		time.sleep(1)
		driver.switch_to.window(tabs[0])
		driver.execute_script(f"nhantien('{id_nv_ttc}')")
		dem_lap = 0
		while True:
			if dem_lap == 10:
				return 0
				break
			try:
				alert = driver.find_element("xpath", "/html/body/div[2]/div/div").text
				result = f"[LIKE PAGE] | {alert} | {result}\n"
				with open("History.txt", "a", encoding="utf-8") as file:
					file.write(result)
				if "thành công" in alert.lower():
					label2.config(text=f"{alert}", fg="green")
				else:
					label2.config(text=f"{alert}", fg="red")
				print(alert)
				break
			except:
				time.sleep(1)
				dem_lap = dem_lap + 1
		time.sleep(2)


def nhiem_vu_follow(max_nv_setting, driver_):
	driver = driver_
	driver.get("https://tuongtaccheo.com/kiemtien/subcheo/")
	time.sleep(7)
	dspost = driver.find_element("id", "dspost").find_elements("tag name", "div")
	max_nv = len(dspost)
	if max_nv > max_nv_setting:
		max_nv = max_nv_setting
	for x in range(1,max_nv+1):
		result = ""
		btn = driver.find_element("xpath", f"/html/body/div/div/div[3]/div/div[1]/div/div[{x}]/div/div/button")
		result = btn.get_attribute("title")
		id_nv_ttc = btn.get_attribute("onclick").split("'")[1]
		url_redirect = result.replace("'", "")
		driver.execute_script(f"like('{id_nv_ttc}', '{url_redirect}')")
		tabs = driver.window_handles
		# Chuyển qua auto fb
		driver.switch_to.window(tabs[1])
		if "about:" in driver.current_url:
			driver.get(url_redirect)
		time.sleep(random.randint(1, 3))
		try:
			lua_chon_button = driver.find_element("xpath", "//div[@role='button' and (contains(@aria-label, 'Xem lựa chọn'))]")
			driver.execute_script("arguments[0].click();", lua_chon_button)
			time.sleep(3)
			follow_button = driver.find_element("xpath", "//div[@role='button' and (contains(@aria-label, 'Theo dõi'))]")
			driver.execute_script("arguments[0].click();", follow_button)
			# follow_button.click()
			print("Tìm thấy nút theo dõi Trong")
			time.sleep(4)
		except:
			try:
				driver.refresh()
				time.sleep(2)
				follow_button = driver.find_element("xpath", "//div[@role='button' and (contains(@aria-label, 'Theo dõi'))]")
				driver.execute_script("arguments[0].click();", follow_button)
				# follow_button.click()
				print("Tìm thấy nút theo dõi Ngoài")
				time.sleep(4)
			except:
				pass
		# Hết auto fb
		time.sleep(2)
		driver.close()
		driver.switch_to.window(tabs[0])
		time.sleep(1)
		driver.execute_script(f"nhantien('{id_nv_ttc}')")
		dem_lap = 0
		while True:
			if dem_lap == 10:
				return 0
				break
			try:
				alert = driver.find_element("xpath", "/html/body/div[2]/div/div").text
				result = f"[LIKE VIP CHEO] | {alert} | {result}\n"
				with open("History.txt", "a", encoding="utf-8") as file:
					file.write(result)
				if "thành công" in alert.lower():
					label2.config(text=f"{alert}", fg="green")
				else:
					label2.config(text=f"{alert}", fg="red")
				print(alert)
				break
			except:
				time.sleep(1)
				dem_lap = dem_lap + 1
		time.sleep(2)


def nhiem_vu_cmt(max_nv_setting, driver_):
	driver = driver_
	driver.get("https://tuongtaccheo.com/kiemtien/cmtcheo/")
	time.sleep(7)
	dspost = driver.find_element("id", "dspost").find_elements("tag name", "div")
	max_nv = len(dspost)
	if max_nv > max_nv_setting:
		max_nv = max_nv_setting
	for x in range(1,max_nv+1):
		result = ""
		btn = driver.find_element("xpath", f"/html/body/div/div/div[2]/div/div[1]/div/div[{x}]/div[1]/div/button")
		div_dscmt = driver.find_element("xpath", f"/html/body/div/div/div[2]/div/div[1]/div/div[{x}]/div[2]")
		dscmt = div_dscmt.find_elements("xpath", ".//textarea")
		noi_dung_cmt = dscmt[random.randint(0, len(dscmt)-1)].text
		result = btn.get_attribute("title")
		id_nv_ttc = btn.get_attribute("onclick").split("'")[1]
		url_redirect = get_redirect_link(result.replace("'", ""))
		driver.execute_script(f"like('{id_nv_ttc}', '{url_redirect}')")
		tabs = driver.window_handles
		# Chuyển qua auto fb
		driver.switch_to.window(tabs[1])
		if "about:" in driver.current_url:
			driver.get(url_redirect)
		time.sleep(random.randint(1, 3))
		driver.implicitly_wait(5)
		try:
			button_mo_cmt = driver.find_element("xpath", "//div[@role='button' and contains(@aria-label, 'comments')]")
			print(f"Có nút mở cmt loai 1")
			button_mo_cmt.click()
			time.sleep(1)
		except:
			pass

		try:
			button_mo_cmt = driver.find_element("xpath", "//div[@role='button' and contains(@aria-label, 'Bình luận')]")
			print(f"Có nút mở cmt loai 2")
			button_mo_cmt.click()
			time.sleep(1)
		except:
			pass
		driver.implicitly_wait(10)
		try:
			input_cmt = driver.find_element("xpath", "//textarea[contains(@placeholder, 'Bình luận')]")
			input_cmt.send_keys(noi_dung_cmt)
			time.sleep(1)
			gui_cmt = driver.find_elements("xpath", "//div[@role='button' and contains(@aria-label, 'Đăng bình luận')]")
			print(f"có {len(gui_cmt)} nút đăng cmt")
			for btn_gui_cmt in gui_cmt:
				print(f"Click nút gửi cmt")
				btn_gui_cmt.click()
			time.sleep(3)
		except:
			pass
		# Hết auto fb
		time.sleep(2)
		driver.close()
		driver.switch_to.window(tabs[0])
		time.sleep(1)
		driver.execute_script(f"nhantien('{id_nv_ttc}')")
		dem_lap = 0
		while True:
			if dem_lap == 10:
				return 0
				break
			try:
				alert = driver.find_element("xpath", "/html/body/div[2]/div/div").text
				result = f"[LIKE VIP CHEO] | {alert} | {result}\n"
				with open("History.txt", "a", encoding="utf-8") as file:
					file.write(result)
				if "thành công" in alert.lower():
					label2.config(text=f"{alert}", fg="green")
				else:
					label2.config(text=f"{alert}", fg="red")
				print(alert)
				break
			except:
				time.sleep(1)
				dem_lap = dem_lap + 1
		time.sleep(2)



def login_ttc(driver_):
	driver = driver_
	max_nv_setting = int(re.sub(r'\D', '', so_nv_entry.get()) or "0")
	time_delay = int(re.sub(r'\D', '', time_delay_entry.get()) or "0")
	so_luong = int(re.sub(r'\D', '', so_luong_entry.get()) or "1")
	if max_nv_setting == 0 or time_delay == 0:
		labelne2.config(text="Lỗi: Chưa cài đặt thông tin", fg="red")
		return 0
	driver.get("https://tuongtaccheo.com/")


def auto_run(driver_):
	driver = driver_
	max_nv_setting = int(re.sub(r'\D', '', so_nv_entry.get()) or "0")
	time_delay = int(re.sub(r'\D', '', time_delay_entry.get()) or "0")
	so_luong = int(re.sub(r'\D', '', so_luong_entry.get()) or "0")
	while True:
		if val_like_vip_post.get() > 0:
			nhiem_vu_like_vip(max_nv_setting, driver)
		if val_like_page.get() > 0:
			nhiem_vu_like_page(max_nv_setting, driver)
		if val_follow.get() > 0:
			nhiem_vu_follow(max_nv_setting, driver)
		if val_cmt.get() > 0:
			nhiem_vu_cmt(max_nv_setting, driver)
		time.sleep(time_delay)
		print("Xong 1 vòng")


trinh_duyet = None

def button1_action():
	global trinh_duyet
	# trinh_duyet = tao_trinh_duyet()
	for trinhduyet in trinh_duyet:
		driver = trinhduyet
		labelne2.config(text="Trạng thái: Đang tiến hành", fg="orange")
		threading.Thread(target=auto_run, args=(driver,), daemon=True).start()


def button2_action():
	global trinh_duyet
	trinh_duyet = tao_trinh_duyet()
	for trinhduyet in trinh_duyet:
		driver = trinhduyet
		labelne2.config(text="Trạng thái: Chờ login TTC & Facebook", fg="blue")
		threading.Thread(target=login_ttc, args=(driver,), daemon=True).start()


def button3_action():
	os.startfile('History.txt')


def on_focus_in(event):
	if event.widget.get() != "" and not bool(re.search(r'\d+', event.widget.get())):
		event.widget.delete(0, tk.END)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Tool tự động cày xu TTC v2")
root.geometry("615x415")  # Tăng chiều cao để chứa dòng chữ mới
# =============== Website chính giữa (CHỈ ĐỊNH NGAY ĐẦU) ===============
labelWebsite = tk.Label(root, text="HandTrickes.com", font=("Arial", 12, "bold"), fg="black", cursor="hand2")
labelWebsite.pack(pady=5)
labelWebsite.bind("<Button-1>", lambda e: webbrowser.open("https://HandTrickes.com"))

# Chia giao diện thành 2 phần
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# ===== Phần trái =====
left_frame = tk.Frame(main_frame, width=200)
left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
left_frame.pack_propagate(False)  # Ngăn frame co giãn

# ===== Phần phải =====
right_frame = tk.Frame(main_frame)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# =============== Phần trái (Thông tin liên hệ) ===============
labelYT = tk.Label(left_frame, text="Youtube: Hoan Lucky", font=("Arial", 11), fg="blue", cursor="hand2", anchor="w")
labelYT.pack(pady=5, fill="x")
labelYT.bind("<Button-1>", lambda e: webbrowser.open("https://www.youtube.com/@HoanLucKy"))

labelZL = tk.Label(left_frame, text="Zalo: 0369723106", font=("Arial", 11), fg="blue", cursor="hand2", anchor="w")
labelZL.pack(pady=5, fill="x")
labelYT.bind("<Button-1>", lambda e: webbrowser.open("https://zalo.me/0369723106"))

labelFB = tk.Label(left_frame, text="Facebook: Lê Công Hoan", font=("Arial", 11), fg="blue", cursor="hand2", anchor="w")
labelFB.pack(pady=5, fill="x")
labelFB.bind("<Button-1>", lambda e: webbrowser.open("https://fb.com/nguoi.phan.boiiii"))

# =============== Phần phải (Nút bấm & Thông báo) ===============
button_frame = tk.Frame(right_frame)
button_frame.pack(pady=10)

val_like_page = tk.IntVar()
val_like_vip_post = tk.IntVar()
val_follow = tk.IntVar()
val_cmt = tk.IntVar()


checkbox_like_page = tk.Checkbutton(button_frame, text="Nhiệm vụ Like Page", variable=val_like_page, font=("Arial", 11))
checkbox_like_page.grid(row=0, column=0, padx=5, columnspan=3, sticky="w")

checkbox_like = tk.Checkbutton(button_frame, text="Nhiệm vụ Like VIP Post", variable=val_like_vip_post, font=("Arial", 11))
checkbox_like.grid(row=1, column=0, padx=5, columnspan=3, sticky="w")

checkbox_follow = tk.Checkbutton(button_frame, text="Nhiệm vụ Follow", variable=val_follow, font=("Arial", 11))
checkbox_follow.grid(row=2, column=0, padx=5, columnspan=3, sticky="w")

checkbox_cmt = tk.Checkbutton(button_frame, text="Nhiệm vụ Bình Luận", variable=val_cmt, font=("Arial", 11))
checkbox_cmt.grid(row=3, column=0, padx=5, columnspan=3, sticky="w")

so_nv_entry = tk.Entry(button_frame, textvariable=tk.StringVar(value="Số nhiệm vụ mỗi vòng lặp"), font=("Arial", 10), width=40)
so_nv_entry.bind("<FocusIn>", on_focus_in)
so_nv_entry.grid(row=4, column=0, pady=5, padx=5, columnspan=3, sticky="w")

time_delay_entry = tk.Entry(button_frame, textvariable=tk.StringVar(value="Thời gian chờ mỗi vòng lặp"), font=("Arial", 10), width=40)
time_delay_entry.bind("<FocusIn>", on_focus_in)
time_delay_entry.grid(row=5, column=0, pady=5, padx=5, columnspan=3, sticky="w")

so_luong_entry = tk.Entry(button_frame, textvariable=tk.StringVar(value="Số luồng cần chạy (mỗi acc chạy một luồng)"), font=("Arial", 10), width=40)
so_luong_entry.bind("<FocusIn>", on_focus_in)
so_luong_entry.grid(row=6, column=0, pady=5, padx=5, columnspan=3, sticky="w")


button2 = tk.Button(button_frame, text="Đăng nhập", command=button2_action, width=10)
button2.grid(row=7, column=0, padx=5)

button1 = tk.Button(button_frame, text="Bắt đầu", command=button1_action, width=10)
button1.grid(row=7, column=1, padx=5)

button3 = tk.Button(button_frame, text="Lịch sử", command=button3_action, width=10)
button3.grid(row=7, column=2, padx=5)

labelne2 = tk.Label(right_frame, text="Trạng thái: chưa bắt đầu", font=("Arial", 10, "bold"), fg="red")
labelne2.pack(pady=6)

label2 = tk.Label(right_frame, text="...", font=("Arial", 9))
label2.pack(pady=6)

# =============== Dòng chữ mới dưới 2 phần chia đôi ===============
labelBottom = tk.Label(root, text="Cảm ơn bạn đã sử dụng công cụ\nĐăng ký kênh để cập nhật tool mới nhất nha", font=("Arial", 10, "italic"), fg="gray")
labelBottom.pack(side="bottom", fill="x", pady=5)  # Căn dưới, chiếm toàn bộ chiều rộng

# Chạy vòng lặp chính
root.mainloop()
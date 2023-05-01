from app.controller import Phong_controller, tour_controller, login_controller, signup_controller, booking_controller, admin_controller
from flask import Flask, render_template, request, redirect, url_for, session
# from flask_login import login_required, LoginManager, UserMixin, login_user
import base64
from datetime import datetime
import re

import qrcode
from io import BytesIO

app = Flask(__name__)

app.config["SECRET_KEY"] = b'_5#y2L"F4Q8z\n\xec]/'


temp_data = {
    'date-start': None,
    'count-date': None,
    'count': None
}

# Khai báo login manager

def base64encode(value):
    return base64.b64encode(value.encode('utf-8')).decode('utf-8')

app.jinja_env.filters['b64encode'] = base64encode

@app.route('/')
def home():
    controller = Phong_controller

    typeroom = controller.get_typeroom()
    service = controller.get_service()
    room = controller.get_room_empty()

    return render_template('home.html' , typeroom = typeroom , services = service , rooms = room)

@app.route('/rooms')
def rooms():
    controller = Phong_controller
    room = controller.get_room()
    return render_template('rooms.html', rooms = room)

@app.route('/events')
def events():
    controller = tour_controller
    tour = controller.get_tour()

    return render_template('events.html' ,tours = tour)
      
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def process_login():
    controller = login_controller

    accounts = controller.get_login()
    username = request.form['username'].upper()
    password = request.form['password'].upper()

    for account in accounts:
        if account[0]== username and account[1] == password:
            session['username'] = username
            session['logged_in'] = True
            return redirect(url_for('home'))
        
    message = "Thông tin không hợp lệ!"
    return render_template('login.html', message=message)

@app.route('/logout', methods=['POST'])
def logout():
    # Xóa thông tin đăng nhập trong session
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('home'))


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def process_signup():
    logincontroller = login_controller
    signupcontroller = signup_controller

    accounts = logincontroller.get_login()

    user_firstname = request.form['user_firstname']
    user_lastname = request.form['user_lastname']
    confirm_password =request.form['confirm-password']
    password = request.form['password']
    user_address = request.form['user_address']
    user_email = request.form['user_email']
    user_phone = request.form['user_phone']
    user_username = request.form['user_username'].upper()

    user_id= request.form['user_id']
    user_fullname = user_lastname + user_firstname

    if len(password) > 50 or len(user_firstname) > 10 or len(user_address) > 100 or len(user_email) > 50 or len(user_phone) > 20 or len(user_username) > 50 or len(user_id) > 20:
        message = "Độ dài thông tin không hợp lệ"
        return render_template('signup.html', message=message)


    if password != confirm_password:
        message = "Xác nhận tài khoản không giống"
        return render_template('signup.html', message=message)

    for account in accounts:
        if account[0] == user_username:
            message = "Tài khoản đã tồn tại"
            return render_template('signup.html', message=message)
        
    save_account, er1= signupcontroller.save_account(user_username, password)
    if er1 == 0:
        save_customer ,er2 = signupcontroller.save_customer(user_id, user_fullname, user_address, user_phone, user_email, user_username)
        if er2 == 0:
            return redirect(url_for('login'))
    message = "Đăng ký thất bại"
    return render_template('signup.html', message=message)
        
@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/room_item')
def room_item():
    type_id = base64.b64decode(request.args.get('TypeId')).decode('utf-8')
    controller = Phong_controller
    rooms = controller.get_typeroom_item(type_id)
    name_type = controller.get_nametype(type_id)
    # rooms[11] = "{:,.0f} đ".format(float(rooms[11])*1000)
    return render_template('rooms_item.html', rooms = rooms, name_type = name_type)

@app.route('/booking')
def booking():
    room_id = base64.b64decode(request.args.get('RoomID')).decode('utf-8')
    Phongcontroller = Phong_controller
    bookingcontroller =booking_controller

    room = Phongcontroller.get_room_item(room_id)
    session['room_id'] = room[0]
    tiennghi = room[4].split(", ")
    Gia = "{:,.0f} đ".format(float(room[11])*1000)
    GiaDC = "{:,.0f} đ".format(float(room[11] * 0.3)*1000)
    GiaCL = "{:,.0f} đ".format(float(room[11] * 0.7)*1000)

 
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    cus_id = bookingcontroller.get_idcus(session['username'])
    cus_info = bookingcontroller.get_infocus(cus_id)
    return render_template('booking.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL =GiaCL, cus_info = cus_info)

@app.route('/booking', methods=['POST'])
def process_booking():
    room_id = base64.b64decode(request.args.get('RoomID')).decode('utf-8')
    controller = Phong_controller
    room = controller.get_room_item(room_id)
    tiennghi = room[4].split(", ")
    Gia = "{:,.0f} đ".format(float(room[11])*1000)
    GiaDC = "{:,.0f} đ".format(float(room[11] * 0.3)*1000)
    GiaCL = "{:,.0f} đ".format(float(room[11] * 0.7)*1000)
    
    date_start = request.form['date-start']
    date_end = request.form['date-end']
    date_format = "%Y-%m-%d"


    if len(date_start) != 0 or len(date_end) != 0:
        date_objs = datetime.strptime(date_start, '%Y-%m-%d')
        date_start_new = date_objs.strftime('%d/%m/%Y')

        date_obje = datetime.strptime(date_end, '%Y-%m-%d')
        date_end_new = date_obje.strftime('%d/%m/%Y')

        date_sn = datetime.strptime(date_start, date_format)
        date_en = datetime.strptime(date_end, date_format)

        delta = date_en - date_sn
        num_days = delta.days
    
    count = request.form['count']
  

    if len(date_start) == 0 or len(date_end) == 0:
        message = "Vui lòng chọn ngày!"
        return render_template('booking.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL =GiaCL, message = message)
    
    if date_objs >= date_obje:
        message = "Số ngày đặt phòng không hợp lệ"
        return render_template('booking.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL =GiaCL, message = message)
    
        message = "Xác nhận email không trùng khớp"
        return render_template('booking.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL =GiaCL, message = message)
    
    temp_data['date-start'] =  date_start_new
    temp_data['count-date'] =  num_days
    temp_data['count'] =  count
    # save_thanhtoan, er1= signupcontroller.save_account(user_username, password)
    # if er1 == 0:
    #     save_customer ,er2 = signupcontroller.save_customer(user_id, user_fullname, user_address, user_phone, user_email, user_username)
    #     if er2 == 0:
    #         return redirect(url_for('login'))
    # message = "Đăng ký thất bại"
    # return render_template('signup.html', message=message)
    
    return redirect(url_for('pay'))

@app.route('/pay')
def pay():
    data = temp_data
    room_id = session['room_id']
    controller = Phong_controller
    room = controller.get_room_item(room_id)
    tiennghi = room[4].split(", ")
    Gia = "{:,.0f} đ".format(float(room[11])*1000)
    GiaCL = "{:,.0f} đ".format(float(room[11] * data['count-date'] * 0.7) * 1000)
    GiaDC = "{:,.0f} đ".format(float(room[11] * data['count-date'] * 0.3) * 1000)
    Tonggia = "{:,.0f} đ".format(float(room[11] * data['count-date']) *1000)
    return render_template('pay.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL = GiaCL,Tonggia = Tonggia)


@app.route('/pay', methods=['POST'])
def process_pay():
    room_id = session['room_id']
    data = temp_data
    Phongcontroller = Phong_controller
    bookingcontroller = booking_controller
    cus_id = bookingcontroller.get_idcus(session['username'])
    room = Phongcontroller.get_room_item(room_id)
    tiennghi = room[4].split(", ")
    Gia = "{:,.0f} đ".format(float(room[11])*1000)
    Tonggia = "{:,.0f} đ".format(float(room[11])* data['count-date'] *1000)
   

    type_pay = request.form['type-pay']   # hình thức thanh toán
    name_pay = request.form['name-pay']   # Tên thẻ
    id_pay = request.form['id-pay']       # Số tín dụng
    datepay = request.form['date-pay']   # Ngày hết hạn

    cvc_pay = request.form['cvc-pay']     # CVC
    phone_zalo = request.form['phone-zalo'] # Thẻ momo
    phone_momo = request.form['phone-momo'] # Thẻ zalo

    GiaCL = "{:,.0f} đ".format(float(room[11] * data['count-date'] * 0.7)*1000)
    GiaDC = "{:,.0f} đ".format(float(room[11] * data['count-date'] * 0.3)*1000)


    if type_pay == 'pay':
        phone_momo = None
        phone_zalo = None
     
        if len(name_pay) == 0:
            message = "Vui lòng nhập Tên thẻ"
            return render_template('pay.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL = GiaCL, Tonggia = Tonggia, message = message)
        
        if len(id_pay) == 0:
            message = "Vui lòng nhập số thẻ tín dụng / thẻ ghi nợ"
            return render_template('pay.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL = GiaCL, Tonggia = Tonggia, message = message)
        
        if len(datepay) == 0:
            message = "Vui lòng nhập số Ngày hết hạn"
            return render_template('pay.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL = GiaCL, Tonggia = Tonggia, message = message)

        if len(cvc_pay) > 3:
            message = "CVC phải là 3 số"
            return render_template('pay.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL = GiaCL, Tonggia = Tonggia, message = message)
        
        date_obj = datetime.strptime(datepay, '%Y-%m-%d')
        date_pay = date_obj.strftime('%d/%m/%Y')
        
    countpay = bookingcontroller.get_countpay()
    countthe = bookingcontroller.get_countthe()
    countmomo = bookingcontroller.get_countmomo()
    countzalo = bookingcontroller.get_countzalo()

    if countpay <= 9:
        matt = 'TT00' + str(countpay + 1)
    elif countpay <= 99:
        matt = 'TT0' + str(countpay + 1)
    else:
        matt = 'TT' + str(countpay + 1)

    if countthe <= 9:
        mathe = 'TT00' + str(countthe + 1)
    elif countthe <= 99:
        mathe = 'TT0' + str(countthe + 1)
    else:
        mathe = 'TT' + str(countthe + 1)

    if countmomo <= 9:
        mamomo = 'TT00' + str(countmomo + 1)
    elif countmomo <= 99:
        mamomo = 'TT0' + str(countmomo + 1)
    else:
        mamomo = 'TT' + str(countmomo + 1)

    if countzalo <= 9:
        mazalo = 'TT00' + str(countzalo + 1)
    elif countzalo <= 99:
        mazalo = 'TT0' + str(countzalo + 1)
    else:
        mazalo = 'TT' + str(countzalo + 1)
        
    if type_pay == 'zalo':
        name_pay = None
        id_pay = None
        date_pay = None
        cvc_pay = None
        phone_momo = None
        if len(phone_zalo) == 0:
            message = "Vui lòng nhập số điện thoại"
            return render_template('pay.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL = GiaCL, Tonggia = Tonggia, message = message)

        if len(phone_zalo) > 13:
            message = "Số điện thoại không hợp lệ "
            return render_template('pay.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL = GiaCL, Tonggia = Tonggia, message = message)
        
        if not re.match(r"^0[1-9][0-9]{8}$", phone_zalo):
            message = "Số điện thoại không hợp lệ "
            return render_template('pay.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL = GiaCL, Tonggia = Tonggia, message = message)

    if type_pay == 'momo':
        name_pay = None
        id_pay = None
        date_pay = None
        cvc_pay = None
        phone_zalo = None

        if len(phone_momo) == 0:
            message = "Vui lòng nhập số điện thoại"
            return render_template('pay.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL = GiaCL, Tonggia = Tonggia, message = message)

        if len(phone_momo) > 13:
            message = "Số điện thoại không hợp lệ "
            return render_template('pay.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL = GiaCL, Tonggia = Tonggia, message = message)
        
        if not re.match(r"^0[1-9][0-9]{8}$", phone_momo):
            message = "Số điện thoại không hợp lệ "
            return render_template('pay.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL = GiaCL, Tonggia = Tonggia, message = message)
    
    result, er= bookingcontroller.save_infopay(matt, type_pay)
    if er == 0:
        if type_pay == 'pay':
            result2, er2 = bookingcontroller.save_pay(mathe, id_pay, name_pay, date_pay, cvc_pay, matt)
            if not er2 == 0:
                return f'<body>{result2}</body>'
            
        if type_pay == 'momo':
            result2, er2 = bookingcontroller.save_momo(mamomo, phone_momo, matt)
            if not er2 == 0:
                return f'<body>{result2}</body>'
            
        if type_pay == 'zalo':
            result2, er2 = bookingcontroller.save_zalo(mazalo, phone_zalo, matt)
            if not er2 == 0:
                return f'<body>{result2}</body>'
            
        countpdp = bookingcontroller.get_countpdp()

        if countpdp <= 9:
            mapdp = '09800' + str(countpdp + 1)
        elif countpdp <= 99:
            mapdp = '0980' + str(countpdp + 1)
        else:
            mapdp = '098' + str(countpdp + 1)     


    tiendc = int(room[11] * data['count-date'] * 0.3)
    result3, er3 = bookingcontroller.save_booking(mapdp, data['date-start'], data['count-date'], data['count'], tiendc, room[0], cus_id, matt)

    if er3 == 0:
        return render_template('success.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaCL = GiaCL, mapdp = mapdp, GiaDC = GiaDC, Tonggia = Tonggia)
        
    return f'<body>không thành công</body>'

@app.route('/success')
def success():
    room_id = session['room_id']

    controller = Phong_controller
    room = controller.get_room_item(room_id)
    tiennghi = room[4].split(", ")

    # bookingcontroller = booking_controller

    # cus_id = bookingcontroller.get_idcus(session['username'])
    # cus_info = bookingcontroller.get_infocus(cus_id)
    
    Gia = "{:,.0f} đ".format(float(room[11])*1000)
    data = temp_data
    Tonggia = "{:,.0f} đ".format(float(room[11] * data['count-date']) *1000)
    GiaCL = "{:,.0f} đ".format(float(room[11] * data['count-date'] * 0.7)*1000)
    GiaDC = "{:,.0f} đ".format(float(room[11] * data['count-date'] * 0.3)*1000)

    return render_template('success.html' , room_item = room , tiennghi = tiennghi, Gia =Gia, GiaDC = GiaDC ,GiaCL = GiaCL, Tonggia = Tonggia)

@app.route('/admin')
def admin():
    roomcontroller = admin_controller
    rooms = roomcontroller.get_room()
    my_list = []
    for room in rooms:
        room_list = list(room)  # chuyển đổi từ tuple sang list
        if room_list[2] == 0:
            room_list[2] = 'Phòng trống'
        elif room_list[2] == 1:
            room_list[2] = 'Phòng đã đặt'
        my_list.append(room_list)  # chuyển đổi lại từ list sang tuple

    return render_template('home_admin.html', rooms=my_list)

@app.route('/delete')
def delete():
    room_id = base64.b64decode(request.args.get('RoomID')).decode('utf-8')
    roomcontroller = Phong_controller
    result, er = roomcontroller.delete_room(room_id)
  
    return f'<body>{er}</body>'


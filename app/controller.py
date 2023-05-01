from ProjectHotel.settings import execute_query

class Phong_controller:
    def get_room_item(maphong):
        sql = "select * from phong ph,loaiphong lp where lp.MALOAIPHONG = ph.LOAIP and ph.MAPHONG = '{0}'".format(maphong)
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result[0]
     
    def get_typeroom():
        sql = "select * from LoaiPhong"
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result
    
    def get_service():
        sql = "select * from dichvu"
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result
    
    def get_room_empty():
        sql = "select * from phong ph,loaiphong lp where lp.MALOAIPHONG = ph.LOAIP and TINHTRANG = 0"
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result
    
    def get_room():
        sql = "select * from phong ph,loaiphong lp where lp.MALOAIPHONG = ph.LOAIP"
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result

    def get_typeroom_item(malp):
        sql = "select * from phong ph join loaiphong lp on lp.MALOAIPHONG = ph.LOAIP where lp.MALOAIPHONG = '{0}'".format(malp)
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result
    
    def get_nametype(malp):
        sql = "select TENLOAIPHONG from LoaiPhong lp where lp.MALOAIPHONG = '{0}'".format(malp)
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result[0][0]
    
    def delete_room(maphong):
        sql = "DELETE FROM PHONG WHERE MAPHONG = '{0}'".format(maphong)
        result, er = execute_query('QLKhachSan', 'a' ,sql)
        return result, er




    
class tour_controller:
    def get_tour():
        sql = "select * from TourDuLich"
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result
    
class login_controller:
    def get_login():
        sql = "select * from taikhoan"
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result
    
class signup_controller:
    def save_customer(cmnd, tenkh, diachi, sdt, email, username):
        sql = "INSERT INTO KhachHang (CMND, TenKH, DiaChi, SDT, Email, Avatar, USERNAME) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 'https://cdn-icons-png.flaticon.com/512/219/219983.png', '{5}')".format(cmnd, tenkh, diachi, sdt, email, username)
        result, er = execute_query('QLKhachSan', 'a' ,sql)
        return result, er
    
    def save_account(username, password):
        sql = "INSERT INTO TaiKhoan (Username, Password, Type) VALUES ('{0}','{1}', 2)".format(username, password)
        result ,er= execute_query('QLKhachSan', 'a' ,sql)
        return result ,er
    
class booking_controller:
    def get_idcus(username):
        sql = "SELECT CMND FROM khachhang where USERNAME = '{0}'".format(username)
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result[0][0]
    
    def get_countpdp():
        sql = "SELECT COUNT(*) FROM PhieuDatPhong"
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result[0][0]
    
    def get_infocus(makh):
        sql = "SELECT * FROM khachhang where CMND = '{0}'".format(makh)
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result[0]
    
    def get_countpay():
        sql = "SELECT COUNT(*) FROM thongtinthanhtoan"
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result[0][0]
    
    def save_infopay(matt, type):
        if type == 'pay':
            type_new = 1

        if type == 'momo':
            type_new = 2

        if type == 'zalo':
            type_new = 3

        sql = "INSERT INTO thongtinthanhtoan VALUES ('{0}','{1}')".format(matt, type_new)
        result ,er= execute_query('QLKhachSan', 'a' ,sql)
        return result ,er
    
    def save_pay(mapay,sothe, tenthe, ngayhethan, cvc, matt):
        sql = "INSERT INTO thenganhang VALUES ('{0}','{1}','{2}', '{3}', '{4}','{5}')".format(mapay, sothe, tenthe, ngayhethan, cvc, matt)
        result ,er= execute_query('QLKhachSan', 'a' ,sql)
        return result ,er
    
    def get_countthe():
        sql = "SELECT COUNT(*) FROM thenganhang"
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result[0][0]
    
    def save_momo(mamomo, sdt, matt):
        sql = "INSERT INTO momo VALUES ('{0}','{1}','{2}')".format(mamomo,sdt, matt)
        result ,er= execute_query('QLKhachSan', 'a' ,sql)
        return result ,er
    
    def get_countmomo():
        sql = "SELECT COUNT(*) FROM momo"
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result[0][0]
    
    def save_zalo(mazalo, sdt, matt):
        sql = "INSERT INTO zalo VALUES ('{0}','{1}','{2}')".format(mazalo,sdt, matt)
        result ,er= execute_query('QLKhachSan', 'a' ,sql)
        return result ,er
    
    def get_countzalo():
        sql = "SELECT COUNT(*) FROM Zalo"
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result[0][0]
    
    def save_booking(mapdp, ngayden, sodem, slng, stc, maphong, makh, matt):
        sql = "INSERT INTO phieudatphong (MAPDP, NGAYDEN, SODEMLUTRU,YEUCAUDACBIET, SOLUONGNGUOI, SOTIENDATCOC,CHECKDC, MAPHONG, MAKH, MATT) VALUES ('{0}', '{1}', '{2}', '', '{3}', '{4}', '', '{5}','{6}','{7}')".format(mapdp, ngayden, sodem, slng, stc, maphong, makh, matt)
        result, er = execute_query('QLKhachSan', 'a' ,sql)
        return result, er
    
class admin_controller():
    def get_room():
        sql ="SELECT * FROM phong ph, loaiphong lp where lp.MALOAIPHONG = ph.loaip"
        result = execute_query('QLKhachSan', 'a' ,sql)
        return result
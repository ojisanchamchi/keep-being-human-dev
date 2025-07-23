---
slug: ruby-arrays-ky-thuat-trung-cap
title: "Nghệ Thuật Xử Lý Mảng Trong Ruby: Kỹ Thuật Trung Cấp Đáng Kinh Ngạc"
authors: [admin]
tags: [ruby, arrays, intermediate]
---

# Nghệ Thuật Xử Lý Mảng Trong Ruby: Kỹ Thuật Trung Cấp Đáng Kinh Ngạc

![Ruby Arrays Intermediate](https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80)

Bạn đã nắm vững các kiến thức cơ bản về mảng trong Ruby? Đã đến lúc nâng cao kỹ năng của bạn với những kỹ thuật trung cấp đầy sức mạnh. Bài viết này sẽ giới thiệu những phương pháp xử lý mảng thông minh hơn, giúp code của bạn trở nên sạch sẽ và hiệu quả hơn.

## 🔪 Cắt mảng với slice, range và chỉ số âm

Ruby cung cấp nhiều cách linh hoạt để cắt và trích xuất phần tử từ mảng:

```ruby
du_lieu = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

# Sử dụng slice với chỉ số bắt đầu và số lượng phần tử
du_lieu.slice(2, 3)      # => ['c', 'd', 'e']

# Sử dụng range
du_lieu[1..4]            # => ['b', 'c', 'd', 'e']
du_lieu[1...4]           # => ['b', 'c', 'd'] (không bao gồm phần tử cuối)

# Sử dụng chỉ số âm
du_lieu[-3..-1]          # => ['e', 'f', 'g']
du_lieu[-5...-2]         # => ['c', 'd', 'e']
```

## 🧠 Tìm kiếm nhị phân với bsearch

Khi làm việc với mảng đã sắp xếp, `bsearch` giúp tìm kiếm phần tử nhanh chóng với độ phức tạp O(log n):

```ruby
so_nguyen = [1, 4, 8, 11, 15, 19, 24, 28, 31, 36, 42]

# Tìm giá trị chính xác
so_nguyen.bsearch { |x| x >= 15 }  # => 15

# Tìm vị trí đầu tiên thỏa mãn điều kiện
vi_tri = so_nguyen.bsearch_index { |x| x >= 30 }  # => 8 (vị trí của số 31)

# Tìm kiếm phức tạp hơn
diem_sinh_vien = [
  {ten: "An", diem: 7.5},
  {ten: "Bình", diem: 8.0},
  {ten: "Cường", diem: 8.5},
  {ten: "Dung", diem: 9.0}
].sort_by { |sv| sv[:diem] }

# Tìm sinh viên đầu tiên có điểm >= 8.5
diem_sinh_vien.bsearch { |sv| sv[:diem] >= 8.5 ? 0 : -1 }  # => {ten: "Cường", diem: 8.5}
```

## 🔄 Chuyển vị ma trận - Biến đổi dữ liệu đa chiều

Phương thức `transpose` cho phép bạn chuyển đổi hàng thành cột và ngược lại trong mảng hai chiều:

```ruby
ma_tran = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
]

ma_tran_chuyen_vi = ma_tran.transpose
# => [
#      [1, 4, 7],
#      [2, 5, 8],
#      [3, 6, 9]
#    ]

# Ứng dụng thực tế: Chuyển đổi dữ liệu CSV
du_lieu_csv = [
  ["Tên", "Tuổi", "Thành phố"],
  ["Minh", "28", "Hà Nội"],
  ["Hương", "25", "Đà Nẵng"],
  ["Tuấn", "30", "TP.HCM"]
]

du_lieu_theo_cot = du_lieu_csv.transpose
# => [
#      ["Tên", "Minh", "Hương", "Tuấn"],
#      ["Tuổi", "28", "25", "30"],
#      ["Thành phố", "Hà Nội", "Đà Nẵng", "TP.HCM"]
#    ]
```

## 🧩 Phân vùng mảng với partition

Phương thức `partition` giúp chia mảng thành hai nhóm dựa trên một điều kiện:

```ruby
so = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Chia thành số chẵn và số lẻ
so_chan, so_le = so.partition { |n| n.even? }
# so_chan = [2, 4, 6, 8, 10]
# so_le = [1, 3, 5, 7, 9]

# Ứng dụng thực tế: Phân loại sinh viên đậu/rớt
diem_thi = [8.5, 6.7, 4.2, 9.0, 5.5, 7.8, 3.9]
dau, rot = diem_thi.partition { |diem| diem >= 5.0 }
# dau = [8.5, 6.7, 9.0, 5.5, 7.8]
# rot = [4.2, 3.9]
```

## 🔗 Kết hợp map và compact trong chuỗi xử lý

Kết hợp các phương thức trong một chuỗi giúp code ngắn gọn và dễ đọc hơn:

```ruby
du_lieu = ["1", "hai", "3", "bốn", "5"]

# Chuyển đổi chuỗi thành số và loại bỏ các giá trị không hợp lệ
so = du_lieu
  .map { |s| Integer(s) rescue nil }
  .compact
# => [1, 3, 5]

# Ứng dụng thực tế: Xử lý dữ liệu từ file CSV
du_lieu_csv = ["12.5", "N/A", "8.75", "error", "10.0"]
gia_tri = du_lieu_csv
  .map { |s| s == "N/A" || s == "error" ? nil : Float(s) rescue nil }
  .compact
# => [12.5, 8.75, 10.0]
```

## 🔍 Truy cập mảng lồng nhau với dig

Phương thức `dig` giúp truy cập an toàn vào các phần tử trong mảng lồng nhau mà không gặp lỗi `NoMethodError`:

```ruby
du_lieu_nguoi_dung = [
  {
    ten: "Minh",
    thong_tin: {
      dia_chi: {
        thanh_pho: "Hà Nội",
        quan: "Cầu Giấy"
      },
      sdt: ["0912345678", "0987654321"]
    }
  },
  {
    ten: "Linh",
    thong_tin: {
      dia_chi: nil,
      sdt: ["0923456789"]
    }
  }
]

# Truy cập an toàn với dig
du_lieu_nguoi_dung[0].dig(:thong_tin, :dia_chi, :thanh_pho)  # => "Hà Nội"
du_lieu_nguoi_dung[1].dig(:thong_tin, :dia_chi, :thanh_pho)  # => nil (không gây lỗi)
```

## 🧮 Tính tổng với block tùy chỉnh

Phương thức `sum` không chỉ dùng để cộng các số, mà còn có thể tùy chỉnh cách tính tổng:

```ruby
san_pham = [
  {ten: "Áo", gia: 250000, so_luong: 2},
  {ten: "Quần", gia: 350000, so_luong: 1},
  {ten: "Giày", gia: 500000, so_luong: 1}
]

# Tính tổng tiền
tong_tien = san_pham.sum { |sp| sp[:gia] * sp[:so_luong] }
# => 1350000

# Tính tổng với giá trị khởi tạo
tong_tien_sau_giam_gia = san_pham.sum(100000) { |sp| sp[:gia] * sp[:so_luong] }
# => 1450000 (thêm 100000 vào tổng)
```

## 🎲 Tạo tổ hợp và tích Descartes với product

Phương thức `product` giúp tạo ra tất cả các cặp phần tử có thể có từ hai hoặc nhiều mảng:

```ruby
mau_ao = ['đỏ', 'xanh', 'trắng']
kich_co = ['S', 'M', 'L', 'XL']

# Tạo tất cả các kết hợp có thể
san_pham = mau_ao.product(kich_co)
# => [
#      ["đỏ", "S"], ["đỏ", "M"], ["đỏ", "L"], ["đỏ", "XL"],
#      ["xanh", "S"], ["xanh", "M"], ["xanh", "L"], ["xanh", "XL"],
#      ["trắng", "S"], ["trắng", "M"], ["trắng", "L"], ["trắng", "XL"]
#    ]

# Tạo tổ hợp phức tạp hơn
chat_lieu = ['cotton', 'kaki']
tat_ca_san_pham = mau_ao.product(kich_co, chat_lieu)
# Kết quả: Mảng 3 chiều với tất cả các kết hợp có thể
```

## 🚀 Kết luận

Các kỹ thuật trung cấp này sẽ giúp bạn xử lý mảng trong Ruby một cách hiệu quả và sáng tạo hơn. Việc nắm vững những phương thức này không chỉ giúp code của bạn ngắn gọn hơn mà còn tăng hiệu suất xử lý dữ liệu.

Hãy thử áp dụng những kỹ thuật này vào dự án của bạn và khám phá sức mạnh thực sự của mảng trong Ruby!

---

Bạn đã sử dụng kỹ thuật nào trong số này? Hãy chia sẻ kinh nghiệm của bạn trong phần bình luận nhé!

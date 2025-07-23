---
slug: ruby-arrays-ky-thuat-nang-cao
title: "Bậc Thầy Xử Lý Mảng Trong Ruby: Những Kỹ Thuật Nâng Cao Đỉnh Cao"
authors: [admin]
tags: [ruby, arrays, advanced]
---

# Bậc Thầy Xử Lý Mảng Trong Ruby: Những Kỹ Thuật Nâng Cao Đỉnh Cao

![Ruby Arrays Advanced](https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80)

Bạn đã thành thạo các kỹ thuật cơ bản và trung cấp về mảng trong Ruby? Đã đến lúc khám phá những kỹ thuật nâng cao, những "vũ khí bí mật" giúp code của bạn trở nên tinh tế, hiệu quả và đẳng cấp hơn. Hãy cùng đi sâu vào thế giới của những bậc thầy Ruby!

<!-- truncate -->

## 🧙‍♂️ Pattern Matching với Mảng - Phép Thuật Mới từ Ruby 3.0

Pattern matching là một trong những tính năng mạnh mẽ nhất được giới thiệu từ Ruby 3.0, giúp bạn trích xuất dữ liệu từ các cấu trúc phức tạp một cách dễ dàng:

```ruby
def phan_tich_du_lieu(data)
  case data
  in [id_nguoi_dung, [nam, thang, ngay], *nhan]
    puts "Người dùng #{id_nguoi_dung} vào ngày #{ngay}/#{thang}/#{nam} với nhãn: #{nhan.inspect}"
  in [id_nguoi_dung, thoi_gian, *]
    puts "Người dùng #{id_nguoi_dung} vào lúc #{thoi_gian}"
  else
    puts "Dữ liệu không hợp lệ"
  end
end

# Sử dụng pattern matching
du_lieu = [42, [2023, 7, 25], 'ruby', 'arrays']
phan_tich_du_lieu(du_lieu)
# => "Người dùng 42 vào ngày 25/7/2023 với nhãn: [\"ruby\", \"arrays\"]"

# Pattern matching trong tham số hàm
def xu_ly_toa_do([(x, y), z])
  puts "Tọa độ 2D: (#{x}, #{y}), Độ cao: #{z}"
end

xu_ly_toa_do([[10, 20], 5])
# => "Tọa độ 2D: (10, 20), Độ cao: 5"
```

## 🔄 Lazy Enumerators - Sức Mạnh của Sự Lười Biếng

Lazy enumerators cho phép bạn xử lý các tập dữ liệu lớn một cách hiệu quả bằng cách chỉ tính toán khi cần thiết:

```ruby
# Tạo một dãy vô hạn các số nguyên tố
require 'prime'
so_nguyen_to_vo_han = Prime.each

# Không hiệu quả và sẽ chạy mãi mãi
# so_nguyen_to_dau = so_nguyen_to_vo_han.take(10)

# Sử dụng lazy để xử lý hiệu quả
so_nguyen_to_lon = so_nguyen_to_vo_han
  .lazy
  .select { |p| p > 1000 }
  .take(5)
  .force
# => [1009, 1013, 1019, 1021, 1031]

# Xử lý tệp lớn theo dòng mà không cần đọc toàn bộ vào bộ nhớ
def doc_va_xu_ly_tep_lon(duong_dan)
  File.open(duong_dan, 'r').each_line
    .lazy
    .map(&:chomp)
    .select { |line| line.include?('ERROR') }
    .take(10)
    .force
end
```

## 🧩 Nhóm Dữ Liệu với each_with_object

Phương thức `each_with_object` cung cấp cách tiếp cận thanh lịch để xây dựng cấu trúc dữ liệu phức tạp:

```ruby
sinh_vien = [
  {ten: "Minh", lop: "12A", diem: 8.5},
  {ten: "Hương", lop: "12A", diem: 9.0},
  {ten: "Tuấn", lop: "12B", diem: 7.5},
  {ten: "Linh", lop: "12B", diem: 8.0},
  {ten: "Nam", lop: "12C", diem: 9.5}
]

# Nhóm sinh viên theo lớp
sinh_vien_theo_lop = sinh_vien.each_with_object({}) do |sv, result|
  (result[sv[:lop]] ||= []) << sv
end
# => {
#      "12A" => [{ten: "Minh", lop: "12A", diem: 8.5}, {ten: "Hương", lop: "12A", diem: 9.0}],
#      "12B" => [{ten: "Tuấn", lop: "12B", diem: 7.5}, {ten: "Linh", lop: "12B", diem: 8.0}],
#      "12C" => [{ten: "Nam", lop: "12C", diem: 9.5}]
#    }

# Tính điểm trung bình theo lớp
diem_trung_binh_theo_lop = sinh_vien.each_with_object({}) do |sv, result|
  lop = sv[:lop]
  result[lop] ||= {tong_diem: 0, so_sv: 0}
  result[lop][:tong_diem] += sv[:diem]
  result[lop][:so_sv] += 1
end.transform_values { |v| v[:tong_diem] / v[:so_sv] }
# => {"12A" => 8.75, "12B" => 7.75, "12C" => 9.5}
```

## 🧠 Tùy Chỉnh Phương Thức uniq với Khối Lệnh

Phương thức `uniq` có thể được tùy chỉnh để xác định "tính duy nhất" dựa trên tiêu chí phức tạp:

```ruby
san_pham = [
  {id: 1, ten: "iPhone", hang: "Apple", gia: 20000000},
  {id: 2, ten: "Galaxy", hang: "Samsung", gia: 18000000},
  {id: 3, ten: "iPhone Pro", hang: "Apple", gia: 30000000},
  {id: 4, ten: "Redmi", hang: "Xiaomi", gia: 5000000}
]

# Lấy sản phẩm duy nhất theo hãng
san_pham_theo_hang = san_pham.uniq { |sp| sp[:hang] }
# => [
#      {id: 1, ten: "iPhone", hang: "Apple", gia: 20000000},
#      {id: 2, ten: "Galaxy", hang: "Samsung", gia: 18000000},
#      {id: 4, ten: "Redmi", hang: "Xiaomi", gia: 5000000}
#    ]

# Ứng dụng thực tế: Lọc email trùng lặp không phân biệt hoa thường
emails = ["user@example.com", "USER@EXAMPLE.COM", "another@gmail.com", "Another@Gmail.com"]
emails_duy_nhat = emails.uniq { |email| email.downcase }
# => ["user@example.com", "another@gmail.com"]
```

## 🧮 Tổ Hợp và Hoán Vị với Mảng

Ruby cung cấp các phương thức mạnh mẽ để làm việc với tổ hợp và hoán vị:

```ruby
nguyen_to = [2, 3, 5, 7]

# Tạo tất cả các tổ hợp có thể có kích thước 2
to_hop = nguyen_to.combination(2).to_a
# => [[2, 3], [2, 5], [2, 7], [3, 5], [3, 7], [5, 7]]

# Tạo tất cả các hoán vị có thể có
hoan_vi = nguyen_to.permutation(3).to_a
# => [[2, 3, 5], [2, 3, 7], [2, 5, 3], [2, 5, 7], [2, 7, 3], [2, 7, 5], ...]

# Ứng dụng thực tế: Tạo tất cả các mật khẩu có thể từ một tập ký tự
ky_tu = ['A', 'B', 'C', '1', '2']
mat_khau_co_the = ky_tu.repeated_permutation(3).map(&:join)
# => ["AAA", "AA1", "AA2", "A1A", "A11", "A12", "A2A", "A21", "A22", ...]
```

## 🔪 Chia Mảng Thành Các Phần Bằng Nhau

Tạo một phương thức để chia mảng thành các phần có kích thước gần bằng nhau:

```ruby
class Array
  def balanced_split(num_chunks)
    return [] if empty?
    
    chunk_size = (size.to_f / num_chunks).ceil
    each_slice(chunk_size).to_a
  end
end

# Chia mảng thành các phần gần bằng nhau
du_lieu = (1..10).to_a
du_lieu.balanced_split(3)
# => [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]]

# Ứng dụng thực tế: Phân chia công việc cho nhiều luồng xử lý
cong_viec = (1..20).to_a
so_luong_worker = 4
cong_viec_theo_worker = cong_viec.balanced_split(so_luong_worker)
# => [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20]]
```

## 🔍 Phân Đoạn Mảng với slice_when

Phương thức `slice_when` cho phép bạn chia mảng thành các phân đoạn dựa trên điều kiện giữa các phần tử liên tiếp:

```ruby
# Phân đoạn mảng số thành các dãy liên tiếp
so = [1, 2, 3, 5, 6, 8, 9, 10, 12]
day_lien_tiep = so.slice_when { |i, j| j != i + 1 }.to_a
# => [[1, 2, 3], [5, 6], [8, 9, 10], [12]]

# Ứng dụng thực tế: Nhóm các giao dịch theo ngày
giao_dich = [
  {ngay: "2023-07-20", so_tien: 100000},
  {ngay: "2023-07-20", so_tien: 200000},
  {ngay: "2023-07-21", so_tien: 150000},
  {ngay: "2023-07-21", so_tien: 300000},
  {ngay: "2023-07-23", so_tien: 500000}
]

giao_dich_theo_ngay = giao_dich.slice_when { |a, b| a[:ngay] != b[:ngay] }.to_a
# => [
#      [{ngay: "2023-07-20", so_tien: 100000}, {ngay: "2023-07-20", so_tien: 200000}],
#      [{ngay: "2023-07-21", so_tien: 150000}, {ngay: "2023-07-21", so_tien: 300000}],
#      [{ngay: "2023-07-23", so_tien: 500000}]
#    ]
```

## 🔄 Xử Lý Mảng Không Đều với Transpose

Khi làm việc với mảng không đều (jagged arrays), phương thức `transpose` tiêu chuẩn sẽ gặp lỗi. Hãy tạo một phiên bản nâng cao:

```ruby
class Array
  def safe_transpose
    return [] if empty?
    
    max_size = map(&:size).max
    map { |row| row.fill(nil, row.size, max_size - row.size) }.transpose
  end
end

# Xử lý mảng không đều
mang_khong_deu = [
  [1, 2, 3],
  [4, 5],
  [6, 7, 8, 9]
]

mang_chuyen_vi = mang_khong_deu.safe_transpose
# => [
#      [1, 4, 6],
#      [2, 5, 7],
#      [3, nil, 8],
#      [nil, nil, 9]
#    ]
```

## 🚀 Xử Lý Dữ Liệu với Pipeline Sử Dụng tap và then

Tạo các pipeline xử lý dữ liệu thanh lịch với `tap` và `then`:

```ruby
# Xử lý dữ liệu theo pipeline
def xu_ly_du_lieu(du_lieu)
  du_lieu
    .then { |data| data.map { |item| item.downcase } }
    .tap { |data| puts "Sau khi chuyển thành chữ thường: #{data.inspect}" }
    .then { |data| data.select { |item| item.length > 3 } }
    .tap { |data| puts "Sau khi lọc theo độ dài: #{data.inspect}" }
    .then { |data| data.map { |item| item.capitalize } }
    .tap { |data| puts "Kết quả cuối cùng: #{data.inspect}" }
end

xu_ly_du_lieu(["RUBY", "JS", "PYTHON", "GO"])
# => Sau khi chuyển thành chữ thường: ["ruby", "js", "python", "go"]
# => Sau khi lọc theo độ dài: ["ruby", "python"]
# => Kết quả cuối cùng: ["Ruby", "Python"]
```

## 🧹 Làm Phẳng Mảng Có Chọn Lọc

Tạo một phương thức để làm phẳng mảng lồng nhau một cách có chọn lọc:

```ruby
class Array
  def selective_flatten(condition)
    each_with_object([]) do |element, result|
      if element.is_a?(Array) && condition.call(element)
        result.concat(element)
      else
        result << element
      end
    end
  end
end

# Làm phẳng có chọn lọc
du_lieu = [1, [2, 3], 4, [5, 6, 7], 8, [9]]
ket_qua = du_lieu.selective_flatten ->(arr) { arr.size > 1 }
# => [1, 2, 3, 4, 5, 6, 7, 8, [9]]

# Ứng dụng thực tế: Làm phẳng cấu trúc dữ liệu phức tạp
cau_truc = [
  {id: 1, ten: "Minh"},
  [
    {id: 2, ten: "Hương"},
    {id: 3, ten: "Tuấn"}
  ],
  {id: 4, ten: "Linh"},
  [
    {id: 5, ten: "Nam"}
  ]
]

nguoi_dung = cau_truc.selective_flatten ->(arr) { arr.all? { |e| e.is_a?(Hash) && e.key?(:id) } }
# => [{id: 1, ten: "Minh"}, {id: 2, ten: "Hương"}, {id: 3, ten: "Tuấn"}, {id: 4, ten: "Linh"}, [{id: 5, ten: "Nam"}]]
```

## 🎯 Kết luận

Những kỹ thuật nâng cao này sẽ giúp bạn xử lý mảng trong Ruby một cách mạnh mẽ và tinh tế hơn. Việc nắm vững và áp dụng chúng không chỉ giúp code của bạn ngắn gọn, dễ đọc mà còn tối ưu hiệu suất xử lý dữ liệu.

Hãy thử nghiệm và kết hợp các kỹ thuật này để tạo ra những giải pháp sáng tạo cho các vấn đề phức tạp trong dự án của bạn!

---

Bạn đã từng áp dụng kỹ thuật nâng cao nào khác khi làm việc với mảng trong Ruby? Hãy chia sẻ kinh nghiệm của bạn trong phần bình luận nhé!

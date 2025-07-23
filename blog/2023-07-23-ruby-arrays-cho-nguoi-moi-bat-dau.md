---
slug: ruby-arrays-cho-nguoi-moi-bat-dau
title: "Khám Phá Mảng Trong Ruby: Hành Trang Cần Thiết Cho Người Mới"
authors: [admin]
tags: [ruby, arrays, beginner]
---

# Khám Phá Mảng Trong Ruby: Hành Trang Cần Thiết Cho Người Mới

![Ruby Arrays](https://images.unsplash.com/photo-1522542550221-31fd19575a2d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80)

Bạn mới bắt đầu với Ruby? Bạn đang loay hoay với khái niệm mảng (arrays)? Đừng lo lắng! Bài viết này sẽ giúp bạn nắm vững những kiến thức cơ bản về mảng trong Ruby một cách dễ dàng và thú vị.

<!-- truncate -->

## 🎮 Tạo mảng - Bước đầu tiên trong cuộc phiêu lưu

Trong Ruby, bạn có thể tạo mảng bằng hai cách chính: sử dụng cú pháp `[]` hoặc constructor `Array.new`. Mỗi cách có ưu điểm riêng tùy vào tình huống sử dụng.

```ruby
# Cách 1: Sử dụng cú pháp []
trai_cay = ['táo', 'chuối', 'cherry']

# Cách 2: Sử dụng Array.new với kích thước cố định
o_trong = Array.new(5)            # => [nil, nil, nil, nil, nil]

# Cách 3: Với giá trị mặc định
so_khong = Array.new(3, 0)        # => [0, 0, 0]
```

## 🔍 Truy cập phần tử - Tìm kho báu trong mảng

Truy cập phần tử trong mảng Ruby rất linh hoạt. Bạn có thể sử dụng chỉ số dương (bắt đầu từ 0) hoặc chỉ số âm (đếm ngược từ cuối mảng).

```ruby
mon_an = ['phở', 'bún chả', 'bánh mì', 'cơm tấm']

# Truy cập bằng chỉ số dương
mon_an[0]      # => 'phở'
mon_an[2]      # => 'bánh mì'

# Truy cập bằng chỉ số âm
mon_an[-1]     # => 'cơm tấm' (phần tử cuối cùng)
mon_an[-3]     # => 'bún chả'

# Phương thức first và last
mon_an.first   # => 'phở'
mon_an.last    # => 'cơm tấm'
```

## 🧩 Thêm và xóa phần tử - Điều chỉnh kho báu của bạn

Ruby cung cấp nhiều phương thức để thêm và xóa phần tử trong mảng:

```ruby
danh_sach = ['học Ruby', 'làm bài tập']

# Thêm phần tử vào cuối mảng
danh_sach.push('đọc sách')        # => ['học Ruby', 'làm bài tập', 'đọc sách']
danh_sach << 'nghe nhạc'          # => ['học Ruby', 'làm bài tập', 'đọc sách', 'nghe nhạc']

# Thêm phần tử vào đầu mảng
danh_sach.unshift('thức dậy sớm') # => ['thức dậy sớm', 'học Ruby', 'làm bài tập', 'đọc sách', 'nghe nhạc']

# Xóa phần tử cuối cùng
phan_tu_cuoi = danh_sach.pop      # => 'nghe nhạc'

# Xóa phần tử đầu tiên
phan_tu_dau = danh_sach.shift     # => 'thức dậy sớm'
```

## 🔄 Lặp qua mảng - Khám phá từng ngóc ngách

Duyệt qua các phần tử trong mảng là một thao tác phổ biến. Ruby cung cấp nhiều cách để thực hiện điều này:

```ruby
mau_sac = ['đỏ', 'xanh lá', 'vàng', 'tím']

# Sử dụng each
mau_sac.each do |mau|
  puts "Tôi thích màu #{mau}"
end

# Sử dụng each_with_index
mau_sac.each_with_index do |mau, index|
  puts "Màu thứ #{index + 1} là: #{mau}"
end
```

## 🧪 Biến đổi mảng - Phép thuật với map và select

Ruby cung cấp các phương thức mạnh mẽ để biến đổi mảng:

```ruby
so = [1, 2, 3, 4, 5]

# Sử dụng map để biến đổi mỗi phần tử
binh_phuong = so.map { |n| n * n }  # => [1, 4, 9, 16, 25]

# Sử dụng select để lọc phần tử
so_chan = so.select { |n| n.even? } # => [2, 4]

# Kết hợp các mảng
so_khac = [6, 7, 8]
tat_ca = so + so_khac              # => [1, 2, 3, 4, 5, 6, 7, 8]
```

## 🧹 Làm sạch mảng - Dọn dẹp kho báu

Đôi khi bạn cần loại bỏ các phần tử không mong muốn:

```ruby
du_lieu = [1, nil, 2, nil, 3, 'a', 'b', nil]

# Loại bỏ nil
du_lieu_sach = du_lieu.compact    # => [1, 2, 3, 'a', 'b']

# Loại bỏ phần tử trùng lặp
mang_trung = [1, 2, 2, 3, 3, 3, 4]
mang_duy_nhat = mang_trung.uniq   # => [1, 2, 3, 4]
```

## 🎯 Kết luận

Mảng là một trong những cấu trúc dữ liệu cơ bản và quan trọng nhất trong Ruby. Nắm vững cách sử dụng mảng sẽ giúp bạn xây dựng các ứng dụng Ruby hiệu quả hơn. Hãy thực hành các ví dụ trên và khám phá thêm các phương thức khác của mảng trong Ruby.

Bạn đã sẵn sàng tiến xa hơn trong hành trình học Ruby? Hãy theo dõi các bài viết tiếp theo của chúng tôi về các chủ đề nâng cao hơn!

---

Bạn có câu hỏi hoặc ý kiến? Hãy để lại bình luận bên dưới nhé!

---
slug: ruby-blocks-tu-co-ban-den-nang-cao
title: Ruby Blocks - Từ Cơ Bản Đến Nâng Cao Cho Developer
authors: [admin]
tags: [ruby, programming, blocks, functional]
---

# Ruby Blocks - Từ Cơ Bản Đến Nâng Cao Cho Developer

Ruby blocks là một trong những tính năng mạnh mẽ nhất của ngôn ngữ Ruby, tạo nên phong cách lập trình độc đáo và linh hoạt. Blocks cho phép bạn đóng gói một đoạn mã để truyền vào các phương thức, tạo ra các API linh hoạt và mã nguồn dễ đọc. Bài viết này sẽ giúp bạn hiểu sâu về blocks trong Ruby, từ khái niệm cơ bản đến các kỹ thuật nâng cao mà các Ruby developer chuyên nghiệp sử dụng hàng ngày.

<!-- truncate -->

## Phần 1: Khái Niệm Cơ Bản Về Ruby Blocks

### Block Là Gì?

Block trong Ruby là một đoạn mã được đóng gói lại, có thể truyền vào phương thức và thực thi sau đó. Block có hai cú pháp phổ biến:

1. Sử dụng `do...end` (thường dùng cho block nhiều dòng):

```ruby
[1, 2, 3].each do |number|
  puts number * 2
end
```

2. Sử dụng dấu ngoặc nhọn `{}` (thường dùng cho block một dòng):

```ruby
[1, 2, 3].each { |number| puts number * 2 }
```

### 🔄 Duyệt Qua Mảng Với each

Phương thức `each` là cách phổ biến nhất để làm việc với collections trong Ruby:

```ruby
colors = ["đỏ", "xanh lá", "xanh dương"]
colors.each do |color|
  puts "Màu: #{color}"
end
# Kết quả:
# Màu: đỏ
# Màu: xanh lá
# Màu: xanh dương
```

### 🔁 Lặp Với times

Phương thức `times` cho phép bạn thực hiện một hành động nhiều lần:

```ruby
5.times do |i|
  puts "Lần lặp thứ #{i + 1}"
end
# Kết quả:
# Lần lặp thứ 1
# Lần lặp thứ 2
# Lần lặp thứ 3
# Lần lặp thứ 4
# Lần lặp thứ 5
```

### 🔍 Lọc Dữ Liệu Với select

Phương thức `select` cho phép bạn lọc các phần tử trong collection dựa trên một điều kiện:

```ruby
numbers = [1, 2, 3, 4, 5, 6]
even_numbers = numbers.select do |number|
  number.even?
end
puts even_numbers.inspect  # [2, 4, 6]
```

### 🔄 Biến Đổi Dữ Liệu Với map

Phương thức `map` cho phép bạn biến đổi mỗi phần tử trong collection:

```ruby
numbers = [1, 2, 3, 4, 5]
squared = numbers.map do |number|
  number * number
end
puts squared.inspect  # [1, 4, 9, 16, 25]
```

### ⚙️ Xây Dựng Phương Thức Tùy Chỉnh Với yield

Bạn có thể định nghĩa các phương thức của riêng mình nhận vào block bằng cách sử dụng `yield`:

```ruby
def chao_hoi
  puts "Trước khi chào hỏi"
  yield if block_given?
  puts "Sau khi chào hỏi"
end

chao_hoi do
  puts "Xin chào từ block!"
end
# Kết quả:
# Trước khi chào hỏi
# Xin chào từ block!
# Sau khi chào hỏi
```

### 🛡️ Bảo Vệ Với block_given?

Phương thức `block_given?` giúp bạn kiểm tra xem một block có được truyền vào phương thức hay không:

```ruby
def thuc_hien_neu_co_block
  if block_given?
    puts "Block được truyền vào, thực thi nó:"
    yield
  else
    puts "Không có block nào được truyền vào"
  end
end

thuc_hien_neu_co_block  # "Không có block nào được truyền vào"
thuc_hien_neu_co_block { puts "Hello!" }  # "Block được truyền vào, thực thi nó:" và "Hello!"
```

### 📁 Quản Lý Tài Nguyên File

Blocks rất hữu ích cho việc quản lý tài nguyên, đảm bảo rằng tài nguyên được giải phóng đúng cách:

```ruby
def doc_file(ten_file)
  file = File.open(ten_file, "r")
  yield(file)
rescue => e
  puts "Lỗi: #{e.message}"
ensure
  file.close if file
end

doc_file("example.txt") do |f|
  puts f.read
end
```

## Phần 2: Kỹ Thuật Trung Cấp Với Ruby Blocks

### 🛠️ Sử Dụng `yield` Với Tham Số

Truyền tham số cho `yield` cho phép người gọi tùy chỉnh hành vi mà không cần tiếp xúc với các biến nội bộ:

```ruby
def voi_ghi_nhat_ky
  thoi_gian_bat_dau = Time.now
  ket_qua = yield
  thoi_gian = Time.now - thoi_gian_bat_dau
  puts "Thực thi trong #{thoi_gian.round(2)}s"
  ket_qua
end

gia_tri = voi_ghi_nhat_ky do
  sleep(0.5)
  "hoàn thành"
end
# => "hoàn thành" và ghi log thời gian thực thi
```

### 🔄 Tạo Iterator Tùy Chỉnh

Bạn có thể tạo iterator của riêng mình bằng cách sử dụng `yield`:

```ruby
def lap_lai_n_lan(n)
  n.times do |i|
    yield(i)
  end
end

lap_lai_n_lan(3) do |i|
  puts "Lần lặp thứ #{i + 1}"
end
# Kết quả:
# Lần lặp thứ 1
# Lần lặp thứ 2
# Lần lặp thứ 3
```

### 🔄 Phương Thức Có Thể Xâu Chuỗi Với Blocks

Bạn có thể tạo các phương thức có thể xâu chuỗi bằng cách trả về `self`:

```ruby
class MyArray
  def initialize(array)
    @array = array
  end
  
  def transform
    @array.map! { |item| yield(item) }
    self
  end
  
  def filter
    @array.select! { |item| yield(item) }
    self
  end
  
  def display
    puts @array.inspect
    self
  end
end

arr = MyArray.new([1, 2, 3, 4, 5])
arr.transform { |n| n * 2 }
   .filter { |n| n > 5 }
   .display
# Kết quả: [6, 8, 10]
```

### 🔍 Kiểm Tra Sự Hiện Diện Của Block

Ngoài `block_given?`, bạn có thể sử dụng các kỹ thuật khác để làm việc với blocks:

```ruby
def thuc_hien_voi_block(&block)
  if block
    puts "Block được truyền vào như một tham số"
    block.call
  else
    puts "Không có block nào được truyền vào"
  end
end

thuc_hien_voi_block { puts "Hello từ block!" }
```

### 🔄 Lọc Và Biến Đổi Collections

Kết hợp `select` và `map` để xử lý dữ liệu phức tạp:

```ruby
users = [
  { name: "Minh", age: 25, active: true },
  { name: "Hoa", age: 17, active: true },
  { name: "Nam", age: 30, active: false }
]

active_user_names = users
  .select { |user| user[:active] }
  .select { |user| user[:age] >= 18 }
  .map { |user| user[:name] }

puts active_user_names.inspect  # ["Minh"]
```

### 🔄 Xử Lý Luồng Điều Khiển Trong Blocks

Bạn có thể sử dụng các câu lệnh điều khiển luồng trong blocks:

```ruby
result = [1, 2, 3, 4, 5].map do |n|
  next 0 if n.even?  # Bỏ qua phần còn lại của block nếu n chẵn
  n * 2
end

puts result.inspect  # [2, 0, 6, 0, 10]
```

## Phần 3: Kỹ Thuật Nâng Cao Với Ruby Blocks

### 🔄 Lazy Infinite Streams Với Enumerator::Lazy

Sử dụng `Enumerator::Lazy` để xây dựng các chuỗi vô hạn, hiệu quả về bộ nhớ:

```ruby
fib = Enumerator.new do |yielder|
  a, b = [0, 1]
  loop do
    yielder << a
    a, b = b, a + b
  end
end.lazy

# Lấy 10 số Fibonacci đầu tiên, map và chọn số chẵn
ket_qua = fib.take(10)
             .map { |n| n * 2 }
             .select(&:even?)

p ket_qua.to_a  # [0, 4, 6, 16, 30]
```

### 🔄 Destructuring Block Parameters

Bạn có thể phân rã các tham số block để làm việc với dữ liệu phức tạp:

```ruby
points = [[1, 2], [3, 4], [5, 6]]

points.each do |(x, y)|
  puts "Điểm: (#{x}, #{y})"
end
# Kết quả:
# Điểm: (1, 2)
# Điểm: (3, 4)
# Điểm: (5, 6)
```

### ⏱️ Benchmark Blocks

Sử dụng blocks để đo hiệu suất mã:

```ruby
def benchmark
  start_time = Time.now
  result = yield
  end_time = Time.now
  puts "Thời gian thực thi: #{(end_time - start_time) * 1000} ms"
  result
end

benchmark do
  # Mã cần đo hiệu suất
  sleep(0.1)
  42
end
```

### 🔄 Retry Với Backoff

Sử dụng blocks để thực hiện các chiến lược retry phức tạp:

```ruby
def with_retry(max_attempts: 3, backoff: ->(n) { n * 2 })
  attempts = 0
  begin
    attempts += 1
    yield
  rescue => e
    if attempts < max_attempts
      sleep_time = backoff.call(attempts)
      puts "Lỗi: #{e.message}. Thử lại sau #{sleep_time}s..."
      sleep(sleep_time)
      retry
    else
      puts "Đã thử #{max_attempts} lần, không thành công."
      raise
    end
  end
end

with_retry do
  # Mã có thể gây ra lỗi
  raise "Lỗi kết nối" if rand < 0.7
  puts "Thành công!"
end
```

### 🔧 Internal DSL Với instance_eval

Sử dụng `instance_eval` để tạo DSL (Domain Specific Language) nội bộ:

```ruby
class FormBuilder
  def initialize
    @fields = []
  end
  
  def build(&block)
    instance_eval(&block)
    self
  end
  
  def text_field(name, options = {})
    @fields << { type: :text, name: name, options: options }
  end
  
  def submit(text)
    @fields << { type: :submit, text: text }
  end
  
  def to_html
    # Tạo HTML từ @fields
    @fields.map { |field| render_field(field) }.join("\n")
  end
  
  private
  
  def render_field(field)
    case field[:type]
    when :text
      "<input type='text' name='#{field[:name]}' />"
    when :submit
      "<button type='submit'>#{field[:text]}</button>"
    end
  end
end

form = FormBuilder.new.build do
  text_field :name, required: true
  text_field :email
  submit "Gửi"
end

puts form.to_html
```

## Phần 4: Kỹ Thuật Chuyên Gia Với Ruby Blocks

### 🔗 Currying Và Composing Procs

Currying biến đổi một `Proc` đa tham số thành một chuỗi các hàm, cho phép áp dụng một phần:

```ruby
# Ví dụ về currying
adder = ->(x, y, z) { x + y + z }.curry
add5and = adder.call(2, 3)   # Proc mong đợi một tham số
puts add5and.call(4)         # => 9

# Helper cho composition
class Proc
  def compose(other)
    ->(*args) { self.call(other.call(*args)) }
  end
end

double = ->(x) { x * 2 }
square = ->(x) { x**2 }
square_then_double = double.compose(square)
puts square_then_double.call(3) # => 18
```

### ⚙️ Dynamic define_method Với Block

Sử dụng `define_method` với blocks để tạo các phương thức động:

```ruby
class DynamicMethods
  OPERATIONS = {
    add: ->(a, b) { a + b },
    subtract: ->(a, b) { a - b },
    multiply: ->(a, b) { a * b },
    divide: ->(a, b) { a / b.to_f }
  }
  
  OPERATIONS.each do |name, operation|
    define_method(name) do |a, b|
      puts "Thực hiện phép #{name} với #{a} và #{b}"
      operation.call(a, b)
    end
  end
end

calc = DynamicMethods.new
puts calc.add(5, 3)      # => 8
puts calc.multiply(5, 3) # => 15
```

### 🔄 Advanced Lazy Enumerator Chaining

Xâu chuỗi các lazy enumerator để xử lý dữ liệu phức tạp một cách hiệu quả:

```ruby
def prime?(num)
  return false if num <= 1
  (2..Math.sqrt(num).to_i).none? { |i| num % i == 0 }
end

# Tạo một chuỗi vô hạn các số nguyên tố
primes = Enumerator.new do |yielder|
  n = 1
  loop do
    n += 1
    yielder << n if prime?(n)
  end
end.lazy

# Tìm 5 số nguyên tố đầu tiên lớn hơn 100 và chia hết cho 3
result = primes
  .select { |p| p > 100 }
  .select { |p| p % 3 == 0 }
  .take(5)

puts result.to_a.inspect # [3, 5, 7, 11, 13]
```

### 🔄 Context Switch Với instance_exec

Sử dụng `instance_exec` để thực thi block trong ngữ cảnh của một đối tượng khác:

```ruby
class User
  attr_accessor :name, :age
  
  def initialize(name, age)
    @name = name
    @age = age
  end
end

class UserFormatter
  def format(user, &block)
    user.instance_exec(&block)
  end
end

user = User.new("Minh", 30)
formatter = UserFormatter.new

result = formatter.format(user) do
  "Tên: #{name}, Tuổi: #{age}"
end

puts result # "Tên: Minh, Tuổi: 30"
```

### 🔄 Block Instrumentation Với Prepend

Sử dụng `prepend` để thêm instrumentation cho các phương thức mà không sửa đổi mã nguồn gốc:

```ruby
module Instrumentation
  def self.instrument(klass, method_name)
    mod = Module.new do
      define_method(method_name) do |*args, &block|
        start_time = Time.now
        result = super(*args, &block)
        end_time = Time.now
        puts "#{klass}##{method_name} mất #{(end_time - start_time) * 1000}ms"
        result
      end
    end
    
    klass.prepend(mod)
  end
end

class SlowCalculator
  def calculate(n)
    sleep(0.1)
    n * 2
  end
end

Instrumentation.instrument(SlowCalculator, :calculate)

calc = SlowCalculator.new
calc.calculate(5) # Sẽ in ra thời gian thực thi
```

## Kết Luận

Ruby blocks là một tính năng mạnh mẽ và linh hoạt, tạo nên phong cách lập trình độc đáo của Ruby. Từ các tác vụ đơn giản như duyệt qua mảng đến các kỹ thuật nâng cao như tạo DSL nội bộ hay xử lý luồng dữ liệu vô hạn, blocks đều đóng vai trò quan trọng.

Khi bạn tiến bộ từ người mới bắt đầu đến chuyên gia Ruby, việc nắm vững và sử dụng thành thạo blocks sẽ giúp bạn viết mã nguồn sạch hơn, linh hoạt hơn và hiệu quả hơn. Blocks không chỉ là một công cụ lập trình mà còn là một triết lý thiết kế, khuyến khích tái sử dụng mã và tách biệt các mối quan tâm.

Hãy thử nghiệm với các ví dụ trong bài viết này và khám phá cách blocks có thể cải thiện mã Ruby của bạn. Đừng ngại sử dụng blocks để tạo ra các API linh hoạt và dễ đọc cho các dự án của mình!

---

*Bài viết này được tổng hợp từ kinh nghiệm thực tế và các tài liệu về Ruby blocks. Nếu bạn có bất kỳ câu hỏi hoặc góp ý nào, hãy để lại bình luận bên dưới.*

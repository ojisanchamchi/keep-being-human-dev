---
slug: ruby-classes-modules-tu-co-ban-den-nang-cao
title: Ruby Classes và Modules - Từ Cơ Bản Đến Nâng Cao Cho Developer
authors: [admin]
tags: [ruby, programming, oop, classes, modules, mixins]
---

# Ruby Classes và Modules - Từ Cơ Bản Đến Nâng Cao Cho Developer

Classes và Modules là hai khái niệm cốt lõi trong Ruby, tạo nên nền tảng của lập trình hướng đối tượng và thiết kế mã nguồn linh hoạt. Hiểu rõ khi nào sử dụng Class và khi nào sử dụng Module sẽ giúp bạn viết mã Ruby hiệu quả và dễ bảo trì hơn. Bài viết này sẽ đưa bạn từ những khái niệm cơ bản đến các kỹ thuật nâng cao mà các Ruby developer chuyên nghiệp sử dụng hàng ngày.

<!-- truncate -->

## Phần 1: Khái Niệm Cơ Bản

### Class Là Gì?

Class trong Ruby là một blueprint (bản thiết kế) để tạo ra các objects. Mỗi class định nghĩa các thuộc tính (attributes) và hành vi (methods) mà các objects của nó sẽ có.

```ruby
class Person
  def initialize(name, age)
    @name = name
    @age = age
  end
  
  def introduce
    "Xin chào, tôi là #{@name}, #{@age} tuổi"
  end
end

# Tạo objects từ class
person1 = Person.new("Minh", 25)
person2 = Person.new("Lan", 30)

puts person1.introduce # => "Xin chào, tôi là Minh, 25 tuổi"
puts person2.introduce # => "Xin chào, tôi là Lan, 30 tuổi"
```

### Module Là Gì?

Module là một cách để nhóm các methods, constants và classes liên quan với nhau. Khác với class, module không thể được instantiate (tạo objects).

```ruby
module Greetings
  def hello
    "Xin chào từ module!"
  end
  
  def goodbye
    "Tạm biệt!"
  end
end

# Module không thể tạo objects
# Greetings.new # => Error!
```

### Sự Khác Biệt Cơ Bản

| Aspect | Class | Module |
|--------|-------|--------|
| Instantiation | Có thể tạo objects | Không thể tạo objects |
| Inheritance | Hỗ trợ inheritance | Không hỗ trợ inheritance |
| Mục đích chính | Tạo objects với state và behavior | Grouping methods, namespacing, mixins |

## Phần 2: Khi Nào Sử Dụng Class vs Module

### Sử Dụng Class Khi:

1. **Cần tạo objects với state riêng biệt**
```ruby
class BankAccount
  def initialize(balance = 0)
    @balance = balance
  end
  
  def deposit(amount)
    @balance += amount
  end
  
  def balance
    @balance
  end
end

account1 = BankAccount.new(1000)
account2 = BankAccount.new(500)
# Mỗi account có state riêng biệt
```

2. **Cần inheritance hierarchy**
```ruby
class Animal
  def speak
    "Some sound"
  end
end

class Dog < Animal
  def speak
    "Woof!"
  end
end

class Cat < Animal
  def speak
    "Meow!"
  end
end
```

### Sử Dụng Module Khi:

1. **Chia sẻ behavior giữa nhiều classes (Mixins)**
```ruby
module Loggable
  def log(message)
    puts "[#{Time.now}] #{message}"
  end
end

class User
  include Loggable
  
  def create
    # logic tạo user
    log("User created")
  end
end

class Order
  include Loggable
  
  def process
    # logic xử lý order
    log("Order processed")
  end
end
```

2. **Tạo namespace để tránh xung đột tên**
```ruby
module PaymentGateway
  class Stripe
    def process_payment
      "Processing via Stripe"
    end
  end
  
  class PayPal
    def process_payment
      "Processing via PayPal"
    end
  end
end

stripe = PaymentGateway::Stripe.new
paypal = PaymentGateway::PayPal.new
```

3. **Tạo utility methods**
```ruby
module MathUtils
  def self.factorial(n)
    return 1 if n <= 1
    n * factorial(n - 1)
  end
  
  def self.fibonacci(n)
    return n if n <= 1
    fibonacci(n - 1) + fibonacci(n - 2)
  end
end

puts MathUtils.factorial(5) # => 120
puts MathUtils.fibonacci(10) # => 55
```

## Phần 3: Kỹ Thuật Trung Cấp

### Include vs Extend vs Prepend

#### Include - Thêm instance methods
```ruby
module Greetable
  def greet
    "Hello from #{self.class}"
  end
end

class Person
  include Greetable
end

person = Person.new
puts person.greet # => "Hello from Person"
```

#### Extend - Thêm class methods
```ruby
module Countable
  def count
    @count ||= 0
    @count += 1
  end
end

class User
  extend Countable
end

puts User.count # => 1
puts User.count # => 2
```

#### Prepend - Thêm methods vào đầu method lookup chain
```ruby
module Trackable
  def save
    puts "Tracking save operation"
    super # Gọi method gốc
  end
end

class Document
  def save
    puts "Saving document"
  end
end

class TrackedDocument < Document
  prepend Trackable
end

TrackedDocument.new.save
# Output:
# Tracking save operation
# Saving document
```

### Module Callbacks và Hooks

```ruby
module Auditable
  def self.included(base)
    puts "#{self} được include vào #{base}"
    base.extend(ClassMethods)
  end
  
  module ClassMethods
    def audited_fields(*fields)
      @audited_fields = fields
    end
    
    def get_audited_fields
      @audited_fields || []
    end
  end
  
  def audit_changes
    self.class.get_audited_fields.each do |field|
      puts "Field #{field} changed"
    end
  end
end

class User
  include Auditable
  
  audited_fields :name, :email
  
  attr_accessor :name, :email
end

user = User.new
user.audit_changes
```

### Concern Pattern (Rails-style)

```ruby
module Timestampable
  extend ActiveSupport::Concern if defined?(ActiveSupport)
  
  included do
    attr_accessor :created_at, :updated_at
    
    def initialize(*args)
      super
      @created_at = Time.now
    end
  end
  
  def touch
    @updated_at = Time.now
  end
  
  module ClassMethods
    def recent(days = 7)
      # Logic để tìm records gần đây
      puts "Finding records from last #{days} days"
    end
  end
end

class Article
  include Timestampable
  
  def initialize(title)
    @title = title
    super()
  end
end

article = Article.new("Ruby Classes và Modules")
article.touch
Article.recent(3)
```

## Phần 4: Kỹ Thuật Nâng Cao

### Dynamic Module và Class Definition

```ruby
# Tạo module động
def create_validator_module(field_name)
  Module.new do
    define_method "validate_#{field_name}" do
      value = instance_variable_get("@#{field_name}")
      raise "#{field_name} không được để trống" if value.nil? || value.empty?
    end
  end
end

class User
  include create_validator_module(:email)
  include create_validator_module(:name)
  
  def initialize(name, email)
    @name = name
    @email = email
  end
end

user = User.new("", "test@example.com")
# user.validate_name # => Error: name không được để trống
```

### Method Missing và Proxy Pattern

```ruby
module DynamicFinder
  def method_missing(method_name, *args)
    if method_name.to_s.start_with?('find_by_')
      field = method_name.to_s.sub('find_by_', '')
      find_by_field(field, args.first)
    else
      super
    end
  end
  
  def respond_to_missing?(method_name, include_private = false)
    method_name.to_s.start_with?('find_by_') || super
  end
  
  private
  
  def find_by_field(field, value)
    puts "Tìm kiếm #{self} với #{field} = #{value}"
    # Logic tìm kiếm thực tế
  end
end

class User
  extend DynamicFinder
end

User.find_by_email("test@example.com")
User.find_by_name("John")
```

### Refinements - Monkey Patching An Toàn

```ruby
module StringExtensions
  refine String do
    def palindrome?
      self == self.reverse
    end
    
    def word_count
      self.split.length
    end
  end
end

class TextAnalyzer
  using StringExtensions
  
  def analyze(text)
    puts "Text: #{text}"
    puts "Word count: #{text.word_count}"
    puts "Is palindrome: #{text.palindrome?}"
  end
end

analyzer = TextAnalyzer.new
analyzer.analyze("madam") # Sử dụng được refined methods

# Bên ngoài class, refined methods không có sẵn
# "test".word_count # => Error!
```

### Eigenclass và Singleton Methods

```ruby
class Person
  def self.species
    "Homo sapiens"
  end
end

# Thêm singleton method cho một object cụ thể
person = Person.new

def person.special_ability
  "Tôi có khả năng đặc biệt!"
end

puts person.special_ability # => "Tôi có khả năng đặc biệt!"

# Object khác không có method này
another_person = Person.new
# another_person.special_ability # => Error!

# Sử dụng eigenclass
person.singleton_class.class_eval do
  def another_special_method
    "Method khác trong eigenclass"
  end
end

puts person.another_special_method
```

### Forwardable Pattern

```ruby
require 'forwardable'

class Team
  extend Forwardable
  
  def initialize
    @members = []
  end
  
  # Delegate methods to @members array
  def_delegators :@members, :<<, :[], :size, :empty?, :each
  def_delegator :@members, :length, :member_count
  
  def add_member(person)
    @members << person
    puts "#{person} đã được thêm vào team"
  end
end

team = Team.new
team.add_member("Alice")
team.add_member("Bob")

puts team.member_count # => 2
puts team.empty? # => false

team.each { |member| puts "Member: #{member}" }
```

## Phần 5: Best Practices và Patterns

### 1. Single Responsibility Principle

```ruby
# ❌ Không tốt - Class có quá nhiều trách nhiệm
class User
  def initialize(name, email)
    @name = name
    @email = email
  end
  
  def save_to_database
    # Logic lưu database
  end
  
  def send_welcome_email
    # Logic gửi email
  end
  
  def generate_report
    # Logic tạo report
  end
end

# ✅ Tốt - Tách thành các modules riêng biệt
module Persistable
  def save_to_database
    puts "Saving #{self.class} to database"
  end
end

module Emailable
  def send_welcome_email
    puts "Sending welcome email to #{@email}"
  end
end

module Reportable
  def generate_report
    puts "Generating report for #{@name}"
  end
end

class User
  include Persistable
  include Emailable
  include Reportable
  
  def initialize(name, email)
    @name = name
    @email = email
  end
end
```

### 2. Composition Over Inheritance

```ruby
# ❌ Inheritance có thể dẫn đến hierarchy phức tạp
class Animal
  def move
    "Moving"
  end
end

class FlyingAnimal < Animal
  def fly
    "Flying"
  end
end

class SwimmingAnimal < Animal
  def swim
    "Swimming"
  end
end

# Vấn đề: Làm sao với động vật vừa bay vừa bơi?

# ✅ Sử dụng modules cho composition
module Flyable
  def fly
    "Flying through the air"
  end
end

module Swimmable
  def swim
    "Swimming in water"
  end
end

module Walkable
  def walk
    "Walking on ground"
  end
end

class Duck
  include Flyable
  include Swimmable
  include Walkable
end

class Fish
  include Swimmable
end

class Bird
  include Flyable
  include Walkable
end

duck = Duck.new
puts duck.fly   # => "Flying through the air"
puts duck.swim  # => "Swimming in water"
puts duck.walk  # => "Walking on ground"
```

### 3. Module Organization Pattern

```ruby
module Authentication
  module TokenGenerator
    def self.generate
      SecureRandom.hex(32)
    end
  end
  
  module Validator
    def self.valid_email?(email)
      email.match?(/\A[\w+\-.]+@[a-z\d\-]+(\.[a-z\d\-]+)*\.[a-z]+\z/i)
    end
  end
  
  module Encryptor
    def self.encrypt(password)
      # Logic mã hóa
      "encrypted_#{password}"
    end
  end
end

# Sử dụng
token = Authentication::TokenGenerator.generate
valid = Authentication::Validator.valid_email?("test@example.com")
encrypted = Authentication::Encryptor.encrypt("password123")
```

## Phần 6: Các Lỗi Thường Gặp và Cách Tránh

### 1. Module Naming Conflicts

```ruby
# ❌ Có thể gây xung đột
module Utils
  def format_date(date)
    date.strftime("%d/%m/%Y")
  end
end

# ✅ Namespace rõ ràng
module DateUtils
  def self.format_vietnamese(date)
    date.strftime("%d/%m/%Y")
  end
  
  def self.format_american(date)
    date.strftime("%m/%d/%Y")
  end
end
```

### 2. Overusing Inheritance

```ruby
# ❌ Inheritance quá sâu
class Vehicle
end

class MotorVehicle < Vehicle
end

class Car < MotorVehicle
end

class SportsCar < Car
end

class Ferrari < SportsCar
end

# ✅ Sử dụng composition
module Engine
  def start_engine
    "Engine started"
  end
end

module GPS
  def navigate_to(destination)
    "Navigating to #{destination}"
  end
end

class Car
  include Engine
  include GPS
  
  def initialize(brand, model)
    @brand = brand
    @model = model
  end
end
```

### 3. Module Method Visibility

```ruby
module Helpers
  def public_helper
    "Available everywhere"
  end
  
  private
  
  def private_helper
    "Only available within including class"
  end
end

class MyClass
  include Helpers
  
  def test
    puts public_helper   # ✅ OK
    puts private_helper  # ✅ OK - private methods từ module
  end
end

obj = MyClass.new
obj.test
# obj.private_helper # ❌ Error - private method
```

## Kết Luận

Classes và Modules là hai công cụ mạnh mẽ trong Ruby, mỗi cái có vai trò và ứng dụng riêng:

**Sử dụng Classes khi:**
- Cần tạo objects với state riêng biệt
- Cần inheritance hierarchy
- Modeling real-world entities

**Sử dụng Modules khi:**
- Chia sẻ behavior giữa nhiều classes
- Tạo namespaces
- Tạo utility methods
- Implement mixins

**Nguyên tắc vàng:**
1. **Composition over Inheritance** - Ưu tiên sử dụng modules để compose behavior
2. **Single Responsibility** - Mỗi class/module chỉ nên có một trách nhiệm chính
3. **Clear Naming** - Đặt tên rõ ràng, tránh xung đột
4. **Proper Organization** - Tổ chức code logic, dễ maintain

Hiểu rõ và áp dụng đúng Classes và Modules sẽ giúp bạn viết Ruby code sạch, linh hoạt và dễ bảo trì. Hãy thực hành thường xuyên và áp dụng các patterns phù hợp với từng tình huống cụ thể trong dự án của bạn.

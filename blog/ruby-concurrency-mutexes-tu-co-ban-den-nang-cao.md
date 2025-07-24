---
slug: ruby-concurrency-mutexes-tu-co-ban-den-nang-cao
title: "Ruby Concurrency & Mutexes: Từ Cơ Bản Đến Nâng Cao - Hướng Dẫn Toàn Diện"
authors: [admin]
tags: [ruby, concurrency, mutex, threading, synchronization, performance, parallel]
---

# Ruby Concurrency & Mutexes: Từ Cơ Bản Đến Nâng Cao

Concurrency (đồng thời) là một trong những chủ đề phức tạp nhất trong lập trình, nhưng cũng là chìa khóa để tạo ra những ứng dụng Ruby hiệu suất cao. Trong bài viết này, chúng ta sẽ khám phá từ những khái niệm cơ bản về threads và mutexes đến các kỹ thuật nâng cao như lock striping và fair mutexes.

<!--truncate-->

## Tại Sao Cần Concurrency?

Trước khi đi vào chi tiết, hãy hiểu tại sao concurrency lại quan trọng:

- **Tăng hiệu suất**: Tận dụng multi-core processors
- **Cải thiện responsiveness**: UI không bị đóng băng khi xử lý tác vụ nặng
- **Xử lý I/O hiệu quả**: Không chờ đợi network/disk operations
- **Scalability**: Xử lý nhiều requests đồng thời
- **Resource utilization**: Tối ưu hóa việc sử dụng CPU và memory

## Vấn Đề Race Conditions

Khi nhiều threads cùng truy cập và thay đổi dữ liệu chung, có thể xảy ra race conditions:

```ruby
# ❌ Không an toàn - Race condition
counter = 0

threads = 5.times.map do
  Thread.new do
    1000.times do
      counter += 1  # Không thread-safe!
    end
  end
end

threads.each(&:join)
puts counter  # Kết quả không đoán trước được, thường < 5000
```

**Vấn đề**: Phép toán `counter += 1` không phải là atomic. Nó bao gồm 3 bước:
1. Đọc giá trị hiện tại
2. Tăng giá trị lên 1
3. Ghi lại giá trị mới

Khi nhiều threads thực hiện đồng thời, có thể dẫn đến mất dữ liệu.

## Phần 1: Cơ Bản - Làm Quen Với Mutex

### 1.1 Bảo Vệ Shared Counter Với Mutex

Mutex (Mutual Exclusion) đảm bảo chỉ có một thread được truy cập critical section tại một thời điểm:

```ruby
require 'thread'

def safe_counter_example
  mutex = Mutex.new
  counter = 0

  threads = 5.times.map do
    Thread.new do
      1000.times do
        mutex.synchronize do
          counter += 1  # Critical section được bảo vệ
        end
      end
    end
  end

  threads.each(&:join)
  puts "Kết quả an toàn: #{counter}"  # => 5000
end

safe_counter_example
```

**Giải thích:**
- `Mutex.new`: Tạo một mutex mới
- `mutex.synchronize`: Khóa mutex, thực thi block, sau đó mở khóa
- Chỉ một thread có thể vào critical section tại một thời điểm

### 1.2 Manual Lock và Unlock

Đôi khi bạn cần kiểm soát chi tiết hơn việc khóa/mở khóa:

```ruby
require 'thread'

class ManualLockExample
  def initialize
    @mutex = Mutex.new
    @data = []
  end

  def safe_update(value)
    @mutex.lock
    begin
      # Critical section
      puts "Thread #{Thread.current.object_id} đang xử lý #{value}"
      @data << value
      sleep(0.01)  # Simulate work
    ensure
      @mutex.unlock  # Luôn unlock trong ensure block
    end
  end

  def get_data
    @mutex.synchronize { @data.dup }
  end
end

# Sử dụng
example = ManualLockExample.new
threads = 5.times.map do |i|
  Thread.new { example.safe_update("data_#{i}") }
end

threads.each(&:join)
puts "Dữ liệu cuối cùng: #{example.get_data}"
```

**Lưu ý quan trọng:**
- Luôn sử dụng `ensure` để đảm bảo mutex được unlock
- Tránh deadlock bằng cách không giữ lock quá lâu

### 1.3 Mutex Per Resource Pattern

Tạo một mutex cho mỗi resource để tránh blocking không cần thiết:

```ruby
require 'thread'

class BankAccount
  def initialize(balance)
    @balance = balance
    @mutex = Mutex.new  # Mỗi account có mutex riêng
  end

  def deposit(amount)
    @mutex.synchronize do
      old_balance = @balance
      sleep(0.01)  # Simulate processing time
      @balance = old_balance + amount
      puts "Gửi #{amount}, số dư mới: #{@balance}"
    end
  end

  def withdraw(amount)
    @mutex.synchronize do
      if @balance >= amount
        old_balance = @balance
        sleep(0.01)
        @balance = old_balance - amount
        puts "Rút #{amount}, số dư mới: #{@balance}"
        true
      else
        puts "Không đủ số dư để rút #{amount}"
        false
      end
    end
  end

  def balance
    @mutex.synchronize { @balance }
  end
end

# Demo
account1 = BankAccount.new(1000)
account2 = BankAccount.new(500)

# Các threads có thể làm việc với different accounts song song
threads = []
threads << Thread.new { account1.deposit(100) }
threads << Thread.new { account2.deposit(200) }
threads << Thread.new { account1.withdraw(50) }
threads << Thread.new { account2.withdraw(300) }

threads.each(&:join)

puts "Account 1 balance: #{account1.balance}"
puts "Account 2 balance: #{account2.balance}"
```

### 1.4 Chờ Threads Hoàn Thành Với Join

`Thread#join` đảm bảo main thread chờ các worker threads hoàn thành:

```ruby
require 'thread'

def demonstrate_join
  mutex = Mutex.new
  results = []
  
  puts "Bắt đầu xử lý..."
  start_time = Time.now

  threads = 4.times.map do |i|
    Thread.new do
      # Simulate different processing times
      processing_time = rand(0.5..2.0)
      sleep(processing_time)
      
      result = "Kết quả từ thread #{i} (#{processing_time.round(2)}s)"
      
      mutex.synchronize do
        results << result
        puts "✓ #{result}"
      end
    end
  end

  # Chờ tất cả threads hoàn thành
  threads.each(&:join)
  
  end_time = Time.now
  puts "\nHoàn thành sau #{(end_time - start_time).round(2)}s"
  puts "Tổng cộng #{results.length} kết quả"
end

demonstrate_join
```

## Phần 2: Trung Cấp - Kỹ Thuật Nâng Cao

### 2.1 Thread-Safe Class Design

Thiết kế class thread-safe từ đầu:

```ruby
require 'thread'

class ThreadSafeCounter
  def initialize(initial_value = 0)
    @count = initial_value
    @mutex = Mutex.new
  end

  def increment(amount = 1)
    @mutex.synchronize do
      old_value = @count
      sleep(0.001)  # Simulate work that could cause race condition
      @count = old_value + amount
    end
  end

  def decrement(amount = 1)
    @mutex.synchronize do
      old_value = @count
      sleep(0.001)
      @count = old_value - amount
    end
  end

  def value
    @mutex.synchronize { @count }
  end

  def reset(new_value = 0)
    @mutex.synchronize { @count = new_value }
  end

  # Atomic operations
  def increment_and_get(amount = 1)
    @mutex.synchronize do
      @count += amount
      @count
    end
  end

  def compare_and_set(expected, new_value)
    @mutex.synchronize do
      if @count == expected
        @count = new_value
        true
      else
        false
      end
    end
  end
end

# Demo
counter = ThreadSafeCounter.new(100)

# Test concurrent operations
threads = []
threads += 10.times.map { Thread.new { 100.times { counter.increment } } }
threads += 5.times.map { Thread.new { 50.times { counter.decrement } } }

threads.each(&:join)

puts "Final value: #{counter.value}"  # Should be 100 + 1000 - 250 = 850
```

### 2.2 Non-Blocking Lock Với try_lock

`Mutex#try_lock` cho phép thử khóa mà không block thread:

```ruby
require 'thread'

class NonBlockingProcessor
  def initialize
    @mutex = Mutex.new
    @processing = false
    @queue = []
  end

  def add_task(task)
    @mutex.synchronize { @queue << task }
  end

  def try_process
    if @mutex.try_lock
      begin
        return false if @processing || @queue.empty?
        
        @processing = true
        task = @queue.shift
        
        puts "#{Thread.current.object_id}: Bắt đầu xử lý #{task}"
        sleep(0.1)  # Simulate work
        puts "#{Thread.current.object_id}: Hoàn thành #{task}"
        
        true
      ensure
        @processing = false
        @mutex.unlock
      end
    else
      puts "#{Thread.current.object_id}: Không thể lấy lock, thử lại sau"
      false
    end
  end

  def queue_size
    @mutex.synchronize { @queue.size }
  end
end

# Demo
processor = NonBlockingProcessor.new

# Add tasks
10.times { |i| processor.add_task("Task_#{i}") }

# Multiple threads try to process
threads = 5.times.map do
  Thread.new do
    10.times do
      success = processor.try_process
      sleep(0.05) unless success
    end
  end
end

threads.each(&:join)
puts "Remaining tasks: #{processor.queue_size}"
```

### 2.3 ConditionVariable - Coordination Between Threads

`ConditionVariable` giúp threads chờ đợi và thông báo cho nhau:

```ruby
require 'thread'

class ProducerConsumerQueue
  def initialize(max_size = 5)
    @queue = []
    @max_size = max_size
    @mutex = Mutex.new
    @not_empty = ConditionVariable.new
    @not_full = ConditionVariable.new
  end

  def produce(item)
    @mutex.synchronize do
      # Chờ cho đến khi queue không full
      while @queue.size >= @max_size
        puts "Producer chờ - Queue full (#{@queue.size}/#{@max_size})"
        @not_full.wait(@mutex)
      end
      
      @queue << item
      puts "Produced: #{item} (Queue: #{@queue.size}/#{@max_size})"
      
      # Thông báo cho consumers
      @not_empty.signal
    end
  end

  def consume
    @mutex.synchronize do
      # Chờ cho đến khi queue không empty
      while @queue.empty?
        puts "Consumer chờ - Queue empty"
        @not_empty.wait(@mutex)
      end
      
      item = @queue.shift
      puts "Consumed: #{item} (Queue: #{@queue.size}/#{@max_size})"
      
      # Thông báo cho producers
      @not_full.signal
      
      item
    end
  end

  def size
    @mutex.synchronize { @queue.size }
  end
end

# Demo
queue = ProducerConsumerQueue.new(3)

# Producer thread
producer = Thread.new do
  10.times do |i|
    queue.produce("Item_#{i}")
    sleep(0.1)
  end
end

# Consumer threads
consumers = 2.times.map do |i|
  Thread.new do
    5.times do
      item = queue.consume
      sleep(0.2)  # Simulate processing
    end
  end
end

producer.join
consumers.each(&:join)
```

### 2.4 Double-Checked Locking Pattern

Tối ưu hóa lazy initialization:

```ruby
require 'thread'

class ConfigurationManager
  @instance = nil
  @mutex = Mutex.new

  def self.instance
    # First check (không cần lock)
    return @instance if @instance

    @mutex.synchronize do
      # Second check (với lock)
      @instance ||= new
    end
  end

  def initialize
    puts "Khởi tạo Configuration..."
    sleep(0.2)  # Simulate expensive initialization
    @config = load_configuration
  end

  private

  def load_configuration
    {
      database: {
        host: 'localhost',
        port: 5432,
        pool_size: 10
      },
      cache: {
        ttl: 3600,
        max_size: 1000
      },
      api: {
        timeout: 30,
        retries: 3
      }
    }
  end

  def config
    @config
  end
end

# Test concurrent access
threads = 10.times.map do |i|
  Thread.new do
    config = ConfigurationManager.instance
    puts "Thread #{i}: #{config.object_id}"
  end
end

threads.each(&:join)
```

## Phần 3: Nâng Cao - Kỹ Thuật Chuyên Nghiệp

### 3.1 Monitor - Reentrant Mutex

Ruby's `Monitor` cho phép cùng một thread lock nhiều lần:

```ruby
require 'monitor'

class ThreadSafeBank
  include MonitorMixin

  def initialize
    super()  # Initialize MonitorMixin
    @accounts = {}
  end

  def create_account(id, initial_balance)
    synchronize do
      @accounts[id] = initial_balance
      log_transaction("Created account #{id} with balance #{initial_balance}")
    end
  end

  def transfer(from_id, to_id, amount)
    synchronize do
      return false unless @accounts[from_id] && @accounts[to_id]
      return false if @accounts[from_id] < amount

      # Nested synchronization - Monitor cho phép reentrant
      withdraw_internal(from_id, amount)
      deposit_internal(to_id, amount)
      
      log_transaction("Transferred #{amount} from #{from_id} to #{to_id}")
      true
    end
  end

  def get_balance(id)
    synchronize { @accounts[id] }
  end

  private

  def withdraw_internal(id, amount)
    synchronize do  # Reentrant lock
      @accounts[id] -= amount
    end
  end

  def deposit_internal(id, amount)
    synchronize do  # Reentrant lock
      @accounts[id] += amount
    end
  end

  def log_transaction(message)
    synchronize do  # Reentrant lock
      puts "[#{Time.now}] #{message}"
    end
  end
end

# Demo
bank = ThreadSafeBank.new
bank.create_account('A', 1000)
bank.create_account('B', 500)

threads = []
threads << Thread.new { bank.transfer('A', 'B', 100) }
threads << Thread.new { bank.transfer('B', 'A', 50) }
threads << Thread.new { puts "Balance A: #{bank.get_balance('A')}" }
threads << Thread.new { puts "Balance B: #{bank.get_balance('B')}" }

threads.each(&:join)
```

### 3.2 Deadlock Prevention

Tránh deadlock bằng ordered locking:

```ruby
require 'thread'

class DeadlockSafeTransfer
  def initialize
    @accounts = {}
    @mutexes = {}
  end

  def create_account(id, balance)
    @accounts[id] = balance
    @mutexes[id] = Mutex.new
  end

  def transfer_safe(from_id, to_id, amount)
    # Luôn lock theo thứ tự object_id để tránh deadlock
    first_id, second_id = [from_id, to_id].sort
    first_mutex = @mutexes[first_id]
    second_mutex = @mutexes[second_id]

    first_mutex.synchronize do
      second_mutex.synchronize do
        if @accounts[from_id] >= amount
          @accounts[from_id] -= amount
          @accounts[to_id] += amount
          puts "Transferred #{amount} from #{from_id} to #{to_id}"
          true
        else
          puts "Insufficient funds in #{from_id}"
          false
        end
      end
    end
  end

  def transfer_with_timeout(from_id, to_id, amount, timeout = 1.0)
    first_id, second_id = [from_id, to_id].sort
    first_mutex = @mutexes[first_id]
    second_mutex = @mutexes[second_id]

    start_time = Time.now

    if first_mutex.try_lock
      begin
        # Try to get second lock with timeout
        while !second_mutex.try_lock
          if Time.now - start_time > timeout
            puts "Transfer timeout: #{from_id} -> #{to_id}"
            return false
          end
          sleep(0.001)
        end

        begin
          if @accounts[from_id] >= amount
            @accounts[from_id] -= amount
            @accounts[to_id] += amount
            puts "Transferred #{amount} from #{from_id} to #{to_id}"
            true
          else
            false
          end
        ensure
          second_mutex.unlock
        end
      ensure
        first_mutex.unlock
      end
    else
      puts "Could not acquire first lock: #{first_id}"
      false
    end
  end

  def balance(id)
    @mutexes[id].synchronize { @accounts[id] }
  end
end

# Demo
bank = DeadlockSafeTransfer.new
bank.create_account('A', 1000)
bank.create_account('B', 800)
bank.create_account('C', 600)

# Concurrent transfers that could cause deadlock with naive locking
threads = []
threads << Thread.new { bank.transfer_safe('A', 'B', 100) }
threads << Thread.new { bank.transfer_safe('B', 'A', 50) }
threads << Thread.new { bank.transfer_safe('B', 'C', 200) }
threads << Thread.new { bank.transfer_safe('C', 'A', 150) }

threads.each(&:join)

puts "Final balances:"
puts "A: #{bank.balance('A')}"
puts "B: #{bank.balance('B')}"
puts "C: #{bank.balance('C')}"
```

## Phần 4: Expert Level - Kỹ Thuật Chuyên Gia

### 4.1 Lock Striping - Sharded Mutex Pool

Để tăng throughput, chia resource thành nhiều shard với mutex riêng:

```ruby
require 'zlib'

class ShardedHashMap
  SHARD_COUNT = 16

  def initialize
    @shards = Array.new(SHARD_COUNT) { {} }
    @mutexes = Array.new(SHARD_COUNT) { Mutex.new }
  end

  def put(key, value)
    idx = shard_index(key)
    @mutexes[idx].synchronize do
      @shards[idx][key] = value
    end
  end

  def get(key)
    idx = shard_index(key)
    @mutexes[idx].synchronize do
      @shards[idx][key]
    end
  end

  def delete(key)
    idx = shard_index(key)
    @mutexes[idx].synchronize do
      @shards[idx].delete(key)
    end
  end

  def size
    total = 0
    @mutexes.each_with_index do |mutex, idx|
      mutex.synchronize do
        total += @shards[idx].size
      end
    end
    total
  end

  # Atomic increment operation
  def increment(key, amount = 1)
    idx = shard_index(key)
    @mutexes[idx].synchronize do
      @shards[idx][key] = (@shards[idx][key] || 0) + amount
    end
  end

  def keys
    all_keys = []
    @mutexes.each_with_index do |mutex, idx|
      mutex.synchronize do
        all_keys.concat(@shards[idx].keys)
      end
    end
    all_keys
  end

  private

  def shard_index(key)
    Zlib.crc32(key.to_s) % SHARD_COUNT
  end
end

# Performance test
def benchmark_sharded_map
  map = ShardedHashMap.new
  
  puts "Testing concurrent writes..."
  start_time = Time.now
  
  threads = 8.times.map do |thread_id|
    Thread.new do
      1000.times do |i|
        key = "thread_#{thread_id}_item_#{i}"
        map.put(key, "value_#{i}")
      end
    end
  end
  
  threads.each(&:join)
  
  end_time = Time.now
  puts "Wrote 8000 items in #{(end_time - start_time).round(3)}s"
  puts "Final size: #{map.size}"
  
  # Test concurrent increments
  puts "\nTesting concurrent increments..."
  start_time = Time.now
  
  threads = 10.times.map do
    Thread.new do
      1000.times do |i|
        map.increment("counter_#{i % 100}")
      end
    end
  end
  
  threads.each(&:join)
  
  end_time = Time.now
  puts "Performed 10000 increments in #{(end_time - start_time).round(3)}s"
end

benchmark_sharded_map
```

### 4.2 Fair FIFO Mutex

Đảm bảo fairness bằng FIFO queue:

```ruby
require 'thread'

class FairMutex
  def initialize
    @queue = []
    @cv = ConditionVariable.new
    @lock = Mutex.new
    @owner = nil
  end

  def synchronize
    thread_id = Thread.current.object_id
    
    @lock.synchronize do
      # Add to queue
      @queue << thread_id
      
      # Wait until it's our turn
      while @queue.first != thread_id || @owner
        @cv.wait(@lock)
      end
      
      # We got the lock
      @owner = thread_id
    end

    begin
      yield
    ensure
      @lock.synchronize do
        @owner = nil
        @queue.shift
        @cv.broadcast  # Wake up all waiting threads
      end
    end
  end

  def queue_length
    @lock.synchronize { @queue.length }
  end
end

# Demo fairness
def demonstrate_fairness
  fair_mutex = FairMutex.new
  results = []
  results_mutex = Mutex.new
  
  threads = 10.times.map do |i|
    Thread.new do
      fair_mutex.synchronize do
        timestamp = Time.now.to_f
        thread_info = "Thread #{i} acquired lock at #{timestamp}"
        
        results_mutex.synchronize do
          results << { thread: i, time: timestamp }
        end
        
        puts thread_info
        sleep(0.1)  # Hold lock briefly
      end
    end
  end
  
  threads.each(&:join)
  
  # Verify FIFO order
  puts "\nVerifying FIFO order:"
  results.sort_by! { |r| r[:time] }
  results.each_with_index do |result, index|
    puts "Position #{index}: Thread #{result[:thread]}"
  end
end

demonstrate_fairness
```

### 4.3 Custom Reentrant Mutex

Tự implement reentrant mutex với ownership tracking:

```ruby
require 'thread'

class CustomReentrantMutex
  def initialize
    @owner = nil
    @depth = 0
    @cv = ConditionVariable.new
    @lock = Mutex.new
  end

  def synchronize
    acquire
    begin
      yield
    ensure
      release
    end
  end

  def acquire
    current_thread = Thread.current
    
    @lock.synchronize do
      if @owner == current_thread
        # Same thread, just increment depth
        @depth += 1
      else
        # Different thread, wait until available
        while @owner
          @cv.wait(@lock)
        end
        @owner = current_thread
        @depth = 1
      end
    end
  end

  def release
    current_thread = Thread.current
    
    @lock.synchronize do
      raise "Not owner" unless @owner == current_thread
      
      @depth -= 1
      if @depth == 0
        @owner = nil
        @cv.signal
      end
    end
  end

  def owned_by_current_thread?
    @lock.synchronize { @owner == Thread.current }
  end

  def lock_depth
    @lock.synchronize { @owner == Thread.current ? @depth : 0 }
  end
end

# Demo reentrant behavior
class ReentrantExample
  def initialize
    @mutex = CustomReentrantMutex.new
    @value = 0
  end

  def method_a
    @mutex.synchronize do
      puts "Method A: depth = #{@mutex.lock_depth}"
      @value += 1
      method_b  # Nested call
    end
  end

  def method_b
    @mutex.synchronize do
      puts "Method B: depth = #{@mutex.lock_depth}"
      @value += 10
      method_c  # Another nested call
    end
  end

  def method_c
    @mutex.synchronize do
      puts "Method C: depth = #{@mutex.lock_depth}"
      @value += 100
    end
  end

  def value
    @mutex.synchronize { @value }
  end
end

example = ReentrantExample.new
example.method_a
puts "Final value: #{example.value}"  # Should be 111
```

### 4.4 Thread Pool With Work Stealing

Advanced pattern cho high-performance concurrent processing:

```ruby
require 'thread'

class WorkStealingThreadPool
  def initialize(size = 4)
    @size = size
    @queues = Array.new(size) { Queue.new }
    @workers = []
    @shutdown = false
    @mutex = Mutex.new
    
    start_workers
  end

  def submit(task)
    return if @shutdown
    
    # Find queue with least work
    min_queue = @queues.min_by(&:size)
    min_queue << task
  end

  def shutdown
    @mutex.synchronize do
      @shutdown = true
      @size.times { |i| @queues[i] << :shutdown }
    end
    
    @workers.each(&:join)
  end

  private

  def start_workers
    @workers = @size.times.map do |worker_id|
      Thread.new { worker_loop(worker_id) }
    end
  end

  def worker_loop(worker_id)
    my_queue = @queues[worker_id]
    
    loop do
      task = get_task(worker_id, my_queue)
      
      case task
      when :shutdown
        break
      when Proc
        begin
          task.call
        rescue => e
          puts "Error in worker #{worker_id}: #{e.message}"
        end
      end
    end
    
    puts "Worker #{worker_id} shutting down"
  end

  def get_task(worker_id, my_queue)
    # Try own queue first
    begin
      return my_queue.pop(true)  # Non-blocking
    rescue ThreadError
      # Queue empty, try work stealing
    end
    
    # Try stealing from other queues
    other_queues = @queues.each_with_index.reject { |_, i| i == worker_id }
    other_queues.each do |queue, _|
      begin
        return queue.pop(true)
      rescue ThreadError
        # This queue is also empty
      end
    end
    
    # All queues empty, block on own queue
    my_queue.pop
  end
end

# Demo
pool = WorkStealingThreadPool.new(4)

# Submit various tasks
20.times do |i|
  pool.submit(proc do
    puts "Processing task #{i} on thread #{Thread.current.object_id}"
    sleep(rand(0.1..0.5))  # Simulate work
    puts "Completed task #{i}"
  end)
end

sleep(3)  # Let tasks complete
pool.shutdown
```

## Best Practices và Lưu Ý

### 1. Tránh Common Pitfalls

```ruby
# ❌ Tránh: Nested locks có thể gây deadlock
def bad_nested_locks
  @lock1.synchronize do
    @lock2.synchronize do
      # Dangerous if another thread locks in reverse order
    end
  end
end

# ✅ Tốt: Ordered locking
def good_ordered_locks
  first, second = [@lock1, @lock2].sort_by(&:object_id)
  first.synchronize do
    second.synchronize do
      # Safe
    end
  end
end

# ❌ Tránh: Giữ lock quá lâu
def bad_long_lock
  @mutex.synchronize do
    expensive_network_call  # Blocks other threads unnecessarily
  end
end

# ✅ Tốt: Minimize lock time
def good_short_lock
  data = expensive_network_call
  @mutex.synchronize do
    @shared_data = data  # Quick update
  end
end
```

### 2. Performance Tips

- **Lock granularity**: Sử dụng fine-grained locks khi có thể
- **Lock-free algorithms**: Cân nhắc atomic operations
- **Thread pool**: Tái sử dụng threads thay vì tạo mới
- **Work stealing**: Cân bằng tải giữa các threads

### 3. Debugging Concurrent Code

```ruby
class DebuggableMutex
  def initialize(name)
    @name = name
    @mutex = Mutex.new
    @owner = nil
    @acquired_at = nil
  end

  def synchronize
    puts "[#{Time.now}] #{Thread.current.object_id} waiting for #{@name}"
    
    @mutex.synchronize do
      @owner = Thread.current.object_id
      @acquired_at = Time.now
      puts "[#{@acquired_at}] #{@owner} acquired #{@name}"
      
      begin
        yield
      ensure
        duration = Time.now - @acquired_at
        puts "[#{Time.now}] #{@owner} released #{@name} (held for #{duration.round(3)}s)"
        @owner = nil
        @acquired_at = nil
      end
    end
  end
end
```

## Kết Luận

Concurrency trong Ruby là một chủ đề phức tạp nhưng cực kỳ quan trọng. Từ những khái niệm cơ bản về Mutex đến các kỹ thuật nâng cao như lock striping và fair mutexes, mỗi technique đều có use case riêng.

### Những điểm chính cần nhớ:

1. **Cơ bản**: Sử dụng `Mutex#synchronize` để bảo vệ critical sections
2. **Trung cấp**: `ConditionVariable` cho thread coordination, `try_lock` cho non-blocking
3. **Nâng cao**: `Monitor` cho reentrant locks, ordered locking để tránh deadlock
4. **Expert**: Lock striping cho performance, custom implementations cho special needs

### Khi nào sử dụng gì:

- **Simple shared state**: `Mutex#synchronize`
- **Producer-consumer**: `ConditionVariable`
- **High contention**: Lock striping hoặc lock-free algorithms
- **Nested locking**: `Monitor` hoặc custom reentrant mutex
- **Fairness required**: Custom FIFO mutex

### Lời khuyên cuối:

- Bắt đầu đơn giản với `Mutex#synchronize`
- Profile trước khi optimize
- Test thoroughly với concurrent workloads
- Document thread safety assumptions
- Consider alternatives như Actor model (Celluloid) hoặc async programming

Concurrency không dễ, nhưng với những kỹ thuật này, bạn có thể xây dựng những ứng dụng Ruby hiệu suất cao và thread-safe! 🚀

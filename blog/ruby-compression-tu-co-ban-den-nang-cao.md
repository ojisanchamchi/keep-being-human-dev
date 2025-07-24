---
slug: ruby-compression-tu-co-ban-den-nang-cao
title: "Ruby Compression: Từ Cơ Bản Đến Nâng Cao - Hướng Dẫn Toàn Diện"
authors: [admin]
tags: [ruby, compression, gzip, zip, performance, optimization, zlib, streaming]
---

# Ruby Compression: Từ Cơ Bản Đến Nâng Cao

Compression (nén dữ liệu) là một kỹ thuật quan trọng trong lập trình, giúp giảm kích thước file, tiết kiệm băng thông và tăng hiệu suất ứng dụng. Trong bài viết này, chúng ta sẽ khám phá các kỹ thuật compression trong Ruby từ cơ bản đến nâng cao, với các ví dụ thực tế và best practices.

<!--truncate-->

## Tại Sao Cần Compression?

Trước khi đi vào chi tiết, hãy hiểu tại sao compression lại quan trọng:

- **Tiết kiệm dung lượng lưu trữ**: Giảm kích thước file trên disk
- **Tăng tốc độ truyền tải**: Giảm thời gian upload/download
- **Giảm băng thông**: Tiết kiệm chi phí network
- **Cải thiện performance**: Faster I/O operations
- **Backup hiệu quả**: Nén dữ liệu backup

## Phần 1: Cơ Bản - Làm Quen Với Compression

### 1.1 Nén File Với Gzip

Ruby cung cấp thư viện `Zlib` built-in để làm việc với compression. Đây là cách đơn giản nhất để nén một file:

```ruby
require 'zlib'

def compress_file_with_gzip(source, destination)
  Zlib::GzipWriter.open(destination) do |gz|
    File.open(source, 'rb') do |file|
      while chunk = file.read(16 * 1024) # Đọc từng chunk 16KB
        gz.write(chunk)
      end
    end
  end
  
  puts "Đã nén #{source} thành #{destination}"
end

# Sử dụng
compress_file_with_gzip('example.txt', 'example.txt.gz')
```

**Giải thích:**
- `Zlib::GzipWriter.open`: Mở file để ghi dữ liệu đã nén
- Đọc file theo chunk để tránh load toàn bộ vào memory
- Block tự động đóng file khi hoàn thành

### 1.2 Tạo ZIP Archive

Để tạo file ZIP chứa nhiều file, chúng ta sử dụng gem `rubyzip`:

```bash
gem install rubyzip
```

```ruby
require 'zip'

def create_zip_archive(files_to_zip, output_zip)
  Zip::File.open(output_zip, Zip::File::CREATE) do |zipfile|
    files_to_zip.each do |filename|
      # Kiểm tra file tồn tại
      if File.exist?(filename)
        zipfile.add(File.basename(filename), filename)
        puts "Đã thêm #{filename} vào archive"
      else
        puts "Cảnh báo: File #{filename} không tồn tại"
      end
    end
  end
end

# Sử dụng
files = ['file1.txt', 'file2.txt', 'data.json']
create_zip_archive(files, 'archive.zip')
```

**Lưu ý quan trọng:**
- Luôn kiểm tra file tồn tại trước khi thêm vào ZIP
- `File.basename()` chỉ lấy tên file, không bao gồm đường dẫn
- Sử dụng block để tự động đóng ZIP file

## Phần 2: Trung Cấp - Kỹ Thuật Nâng Cao

### 2.1 Nén String Trong Memory

Đối với dữ liệu tạm thời như JSON payload hoặc cache, nén trong memory sẽ nhanh hơn:

```ruby
require 'zlib'

def compress_string_in_memory(data, level: Zlib::BEST_COMPRESSION)
  # Nén dữ liệu
  compressed = Zlib::Deflate.deflate(data, level)
  
  puts "Kích thước gốc: #{data.bytesize} bytes"
  puts "Kích thước sau nén: #{compressed.bytesize} bytes"
  puts "Tỷ lệ nén: #{((1 - compressed.bytesize.to_f / data.bytesize) * 100).round(2)}%"
  
  compressed
end

def decompress_string(compressed_data)
  Zlib::Inflate.inflate(compressed_data)
end

# Ví dụ với JSON data
json_data = {
  users: (1..1000).map { |i| 
    { id: i, name: "User #{i}", email: "user#{i}@example.com" }
  }
}.to_json

compressed = compress_string_in_memory(json_data)
decompressed = decompress_string(compressed)

puts "Dữ liệu khôi phục chính xác: #{decompressed == json_data}"
```

**Các mức độ nén:**
- `Zlib::NO_COMPRESSION`: Không nén (0)
- `Zlib::BEST_SPEED`: Nén nhanh nhất (1)
- `Zlib::DEFAULT_COMPRESSION`: Cân bằng (6)
- `Zlib::BEST_COMPRESSION`: Nén tốt nhất (9)

### 2.2 Nén và Giải Nén File Streaming

Phương pháp streaming giúp xử lý file lớn mà không cần load toàn bộ vào memory:

```ruby
require 'zlib'

class FileCompressor
  CHUNK_SIZE = 16 * 1024 # 16KB chunks
  
  def self.compress_file(input_path, output_path)
    File.open(input_path, 'rb') do |input|
      Zlib::GzipWriter.open(output_path) do |gz|
        while chunk = input.read(CHUNK_SIZE)
          gz.write(chunk)
        end
      end
    end
    
    original_size = File.size(input_path)
    compressed_size = File.size(output_path)
    compression_ratio = ((1 - compressed_size.to_f / original_size) * 100).round(2)
    
    puts "Nén hoàn thành:"
    puts "  File gốc: #{format_bytes(original_size)}"
    puts "  File nén: #{format_bytes(compressed_size)}"
    puts "  Tỷ lệ nén: #{compression_ratio}%"
  end
  
  def self.decompress_file(input_path, output_path)
    Zlib::GzipReader.open(input_path) do |gz|
      File.open(output_path, 'wb') do |output|
        while chunk = gz.read(CHUNK_SIZE)
          output.write(chunk)
        end
      end
    end
    
    puts "Giải nén hoàn thành: #{output_path}"
  end
  
  private
  
  def self.format_bytes(bytes)
    units = ['B', 'KB', 'MB', 'GB']
    size = bytes.to_f
    unit_index = 0
    
    while size >= 1024 && unit_index < units.length - 1
      size /= 1024
      unit_index += 1
    end
    
    "#{size.round(2)} #{units[unit_index]}"
  end
end

# Sử dụng
FileCompressor.compress_file('large_file.log', 'large_file.log.gz')
FileCompressor.decompress_file('large_file.log.gz', 'restored_file.log')
```

## Phần 3: Nâng Cao - Kỹ Thuật Chuyên Nghiệp

### 3.1 Tạo TAR.GZ Archives

Để tạo archive với metadata và permissions, kết hợp `Archive::Tar::Minitar` với `Zlib`:

```bash
gem install minitar
```

```ruby
require 'zlib'
require 'archive/tar/minitar'
include Archive::Tar

class TarGzArchiver
  def self.create_archive(sources, output_path, compression_level: Zlib::BEST_COMPRESSION)
    Zlib::GzipWriter.open(output_path, compression_level) do |gzip|
      Minitar::Writer.open(gzip) do |tar|
        sources.each do |path|
          if File.directory?(path)
            puts "Thêm thư mục: #{path}"
            Minitar.pack_dir(path, tar)
          elsif File.file?(path)
            puts "Thêm file: #{path}"
            Minitar.pack_file(path, tar)
          else
            puts "Cảnh báo: #{path} không tồn tại"
          end
        end
      end
    end
    
    puts "Tạo archive thành công: #{output_path}"
  end
  
  def self.extract_archive(archive_path, destination_dir)
    Dir.mkdir(destination_dir) unless Dir.exist?(destination_dir)
    
    Zlib::GzipReader.open(archive_path) do |gzip|
      Minitar::Reader.open(gzip) do |tar|
        tar.each do |entry|
          destination_path = File.join(destination_dir, entry.full_name)
          
          if entry.directory?
            Dir.mkdir(destination_path) unless Dir.exist?(destination_path)
          else
            File.open(destination_path, 'wb') do |file|
              file.write(entry.read)
            end
            # Khôi phục permissions
            File.chmod(entry.mode, destination_path)
          end
          
          puts "Giải nén: #{entry.full_name}"
        end
      end
    end
    
    puts "Giải nén hoàn thành vào: #{destination_dir}"
  end
end

# Sử dụng
sources = ['app/', 'config/', 'README.md']
TarGzArchiver.create_archive(sources, 'backup.tar.gz')
TarGzArchiver.extract_archive('backup.tar.gz', 'restored/')
```

### 3.2 Streaming Large File Compression

Đối với file rất lớn, cần tối ưu hóa memory usage và performance:

```ruby
require 'zlib'

class LargeFileCompressor
  DEFAULT_BUFFER_SIZE = 64 * 1024 # 64KB buffer
  
  def initialize(buffer_size: DEFAULT_BUFFER_SIZE)
    @buffer_size = buffer_size
  end
  
  def compress_large_file(input_path, output_path, level: Zlib::BEST_SPEED)
    start_time = Time.now
    bytes_processed = 0
    
    File.open(input_path, 'rb') do |input|
      Zlib::GzipWriter.open(output_path, level) do |gz|
        while chunk = input.read(@buffer_size)
          gz.write(chunk)
          bytes_processed += chunk.bytesize
          
          # Progress reporting
          if bytes_processed % (1024 * 1024) == 0 # Mỗi 1MB
            print "\rĐã xử lý: #{format_bytes(bytes_processed)}"
          end
        end
      end
    end
    
    end_time = Time.now
    processing_time = end_time - start_time
    
    original_size = File.size(input_path)
    compressed_size = File.size(output_path)
    
    puts "\n\nThống kê nén:"
    puts "  Thời gian xử lý: #{processing_time.round(2)}s"
    puts "  Tốc độ: #{format_bytes(original_size / processing_time)}/s"
    puts "  Kích thước gốc: #{format_bytes(original_size)}"
    puts "  Kích thước nén: #{format_bytes(compressed_size)}"
    puts "  Tỷ lệ nén: #{((1 - compressed_size.to_f / original_size) * 100).round(2)}%"
  end
  
  private
  
  def format_bytes(bytes)
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = bytes.to_f
    unit_index = 0
    
    while size >= 1024 && unit_index < units.length - 1
      size /= 1024
      unit_index += 1
    end
    
    "#{size.round(2)} #{units[unit_index]}"
  end
end

# Sử dụng
compressor = LargeFileCompressor.new(buffer_size: 128 * 1024) # 128KB buffer
compressor.compress_large_file('huge_video.mp4', 'huge_video.mp4.gz')
```

## Phần 4: Expert Level - Kỹ Thuật Chuyên Gia

### 4.1 Custom Streaming Chunked Compression

Đây là kỹ thuật nâng cao nhất, cho phép kiểm soát hoàn toàn quá trình compression:

```ruby
require 'zlib'

class AdvancedStreamCompressor
  CHUNK_SIZE = 16 * 1024 # 16KB per chunk
  
  def self.compress_with_metadata(input_path, output_path, level: Zlib::BEST_COMPRESSION)
    File.open(input_path, 'rb') do |infile|
      File.open(output_path, 'wb') do |outfile|
        gz = Zlib::GzipWriter.new(outfile, level)
        
        # Tùy chỉnh Gzip header với metadata
        gz.orig_name = File.basename(input_path)
        gz.mtime = File.mtime(input_path).to_i
        gz.comment = "Compressed by Ruby Advanced Compressor"
        
        # Streaming compression với progress tracking
        total_size = File.size(input_path)
        processed = 0
        
        while chunk = infile.read(CHUNK_SIZE)
          gz.write(chunk)
          processed += chunk.bytesize
          
          # Progress bar
          progress = (processed.to_f / total_size * 100).round(1)
          print "\rProgress: #{progress}% [#{format_progress_bar(progress)}]"
        end
        
        gz.close
        puts "\nHoàn thành!"
      end
    end
  end
  
  def self.benchmark_compression_levels(input_path)
    puts "Benchmark các mức độ nén cho file: #{File.basename(input_path)}"
    puts "=" * 60
    
    levels = [
      [Zlib::BEST_SPEED, "BEST_SPEED"],
      [Zlib::DEFAULT_COMPRESSION, "DEFAULT"],
      [Zlib::BEST_COMPRESSION, "BEST_COMPRESSION"]
    ]
    
    original_size = File.size(input_path)
    
    levels.each do |level, name|
      output_path = "#{input_path}.#{name.downcase}.gz"
      
      start_time = Time.now
      compress_with_metadata(input_path, output_path, level: level)
      end_time = Time.now
      
      compressed_size = File.size(output_path)
      compression_ratio = ((1 - compressed_size.to_f / original_size) * 100).round(2)
      processing_time = (end_time - start_time).round(2)
      
      puts "\n#{name}:"
      puts "  Thời gian: #{processing_time}s"
      puts "  Kích thước: #{format_bytes(compressed_size)}"
      puts "  Tỷ lệ nén: #{compression_ratio}%"
      puts "  Tốc độ: #{format_bytes(original_size / processing_time)}/s"
      puts
      
      # Cleanup
      File.delete(output_path)
    end
  end
  
  private
  
  def self.format_progress_bar(progress, width: 30)
    filled = (progress / 100.0 * width).round
    empty = width - filled
    "█" * filled + "░" * empty
  end
  
  def self.format_bytes(bytes)
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = bytes.to_f
    unit_index = 0
    
    while size >= 1024 && unit_index < units.length - 1
      size /= 1024
      unit_index += 1
    end
    
    "#{size.round(2)} #{units[unit_index]}"
  end
end

# Sử dụng
AdvancedStreamCompressor.benchmark_compression_levels('large_dataset.csv')
```

### 4.2 Multi-threaded Compression

Đối với hệ thống multi-core, có thể tăng tốc bằng parallel processing:

```ruby
require 'zlib'
require 'thread'

class ParallelCompressor
  def self.compress_multiple_files(file_list, output_dir, max_threads: 4)
    Dir.mkdir(output_dir) unless Dir.exist?(output_dir)
    
    queue = Queue.new
    file_list.each { |file| queue << file }
    
    threads = []
    mutex = Mutex.new
    completed = 0
    
    max_threads.times do
      threads << Thread.new do
        while !queue.empty?
          begin
            file_path = queue.pop(true) # non-blocking pop
            output_path = File.join(output_dir, "#{File.basename(file_path)}.gz")
            
            compress_single_file(file_path, output_path)
            
            mutex.synchronize do
              completed += 1
              puts "Hoàn thành #{completed}/#{file_list.length}: #{File.basename(file_path)}"
            end
          rescue ThreadError
            # Queue empty
            break
          end
        end
      end
    end
    
    threads.each(&:join)
    puts "Nén song song hoàn thành!"
  end
  
  private
  
  def self.compress_single_file(input_path, output_path)
    Zlib::GzipWriter.open(output_path, Zlib::BEST_SPEED) do |gz|
      File.open(input_path, 'rb') do |file|
        while chunk = file.read(16 * 1024)
          gz.write(chunk)
        end
      end
    end
  end
end

# Sử dụng
files = Dir.glob("logs/*.log")
ParallelCompressor.compress_multiple_files(files, "compressed_logs", max_threads: 8)
```

## Best Practices và Lưu Ý

### 1. Chọn Mức Độ Nén Phù Hợp

```ruby
# Cho real-time applications
level = Zlib::BEST_SPEED

# Cho storage/backup
level = Zlib::BEST_COMPRESSION

# Cân bằng tốc độ và kích thước
level = Zlib::DEFAULT_COMPRESSION
```

### 2. Memory Management

```ruby
# ✅ Tốt: Streaming với chunk size hợp lý
CHUNK_SIZE = 16 * 1024 # 16KB

# ❌ Tránh: Load toàn bộ file vào memory
data = File.read(large_file) # Có thể gây OOM
```

### 3. Error Handling

```ruby
def safe_compress(input_path, output_path)
  begin
    Zlib::GzipWriter.open(output_path) do |gz|
      File.open(input_path, 'rb') do |file|
        while chunk = file.read(16 * 1024)
          gz.write(chunk)
        end
      end
    end
    puts "Nén thành công: #{output_path}"
  rescue Errno::ENOENT
    puts "Lỗi: File không tồn tại - #{input_path}"
  rescue Zlib::Error => e
    puts "Lỗi compression: #{e.message}"
    File.delete(output_path) if File.exist?(output_path)
  rescue => e
    puts "Lỗi không xác định: #{e.message}"
  end
end
```

### 4. Performance Tips

- Sử dụng buffer size là bội số của 2 (16KB, 32KB, 64KB)
- Chọn compression level phù hợp với use case
- Với file lớn, ưu tiên `BEST_SPEED` để giảm CPU usage
- Monitor memory usage khi xử lý file lớn
- Sử dụng parallel processing cho multiple files

## Kết Luận

Compression trong Ruby là một kỹ năng quan trọng cho mọi developer. Từ việc nén file đơn giản với Gzip đến các kỹ thuật streaming phức tạp, Ruby cung cấp đầy đủ công cụ để xử lý mọi tình huống.

Những điểm chính cần nhớ:

1. **Cơ bản**: Sử dụng `Zlib` cho Gzip và `rubyzip` cho ZIP
2. **Trung cấp**: Streaming để xử lý file lớn, nén in-memory cho dữ liệu tạm
3. **Nâng cao**: TAR.GZ archives với metadata, parallel processing
4. **Expert**: Custom streaming với progress tracking và optimization

Hãy lựa chọn kỹ thuật phù hợp với nhu cầu cụ thể của dự án và luôn cân nhắc giữa tốc độ nén và kích thước file đầu ra.

Chúc các bạn áp dụng thành công các kỹ thuật compression trong Ruby! 🚀

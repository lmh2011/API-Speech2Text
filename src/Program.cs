using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        // URL của API nhận dạng giọng nói
        string url = "http://127.0.0.1:8000/speech-to-text/";

        // Đường dẫn tới tệp âm thanh cần chuyển đổi
        string audioFilePath = "speaker_a.wav";

        try
        {
            // Đọc dữ liệu âm thanh dưới dạng nhị phân
            byte[] audioData = await File.ReadAllBytesAsync(audioFilePath);

            using (HttpClient client = new HttpClient())
            {
                // Cấu hình tiêu đề yêu cầu
                var content = new ByteArrayContent(audioData);
                content.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");

                // Gửi yêu cầu POST với dữ liệu âm thanh
                HttpResponseMessage response = await client.PostAsync(url, content);

                // Kiểm tra phản hồi
                if (response.IsSuccessStatusCode)
                {
                    // Đọc phản hồi từ API
                    string responseContent = await response.Content.ReadAsStringAsync();
                    Console.WriteLine("Phản hồi từ API:");
                    Console.WriteLine(responseContent);
                }
                else
                {
                    Console.WriteLine($"Lỗi: API trả về mã trạng thái {response.StatusCode}");
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Đã xảy ra lỗi: {ex.Message}");
        }
    }
}

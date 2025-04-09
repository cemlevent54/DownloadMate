using downloadmate.helper;
using downloadmate.webview;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace downloadmate.api
{
    public class DownloaderClient
    {
        private readonly HttpClient httpClient;

        public DownloaderClient()
        {
            httpClient = new HttpClient
            {
                Timeout = TimeSpan.FromMinutes(3) // ⏱ 5 dakika timeout
            };
        }

        public async Task<string> DownloadFileAsync(string platform, string url, string type, string cookies = "", string fileName = "")
        {
            var baseUrl = EnvReader.Get("API_URL");
            var requestUrl = $"{baseUrl}/{platform}/download";

            // 🍪 Cookie otomatik yükleme
            if (string.IsNullOrWhiteSpace(cookies))
            {
                cookies = platform switch
                {
                    "youtube" => GlobalCookies.LoadYouTubeCookies(),
                    "instagram" => GlobalCookies.LoadInstagramCookies(),
                    _ => ""
                };
            }

            var requestBody = new
            {
                url = url,
                type = type
            };

            var requestJson = JsonSerializer.Serialize(requestBody);
            var content = new StringContent(requestJson, Encoding.UTF8, "application/json");

            if (!string.IsNullOrEmpty(cookies))
            {
                content.Headers.Add("cookie", cookies);
            }

            var response = await httpClient.PostAsync(requestUrl, content);

            if (!response.IsSuccessStatusCode)
            {
                throw new Exception($"API Error: {await response.Content.ReadAsStringAsync()}");
            }

            var originalFilename = response.Content.Headers.ContentDisposition?.FileName?.Trim('"') ?? "downloaded_file";
            var fileBytes = await response.Content.ReadAsByteArrayAsync();

            // ✅ Uzantıyı koruyarak yeniden adlandırma
            string finalFilename = string.IsNullOrWhiteSpace(fileName)
                ? originalFilename
                : fileName + Path.GetExtension(originalFilename);

            var finalPath = DownloadPathHelper.GetFilePath(finalFilename);

            Directory.CreateDirectory(Path.GetDirectoryName(finalPath)!);
            await File.WriteAllBytesAsync(finalPath, fileBytes);

            return finalPath;
        }


    }
}

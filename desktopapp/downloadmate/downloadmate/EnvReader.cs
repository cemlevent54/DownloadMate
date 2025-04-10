using System;
using System.Collections.Generic;
using System.IO;

namespace downloadmate
{
    public static class EnvReader
    {
        private static Dictionary<string, string> envValues = new();

        // static constructor sadece 1 kez çalışır ve LoadEnv'i çağırır
        static EnvReader()
        {
            LoadEnv();
        }

        private static void LoadEnv()
        {
            string envPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, ".env");

            if (!File.Exists(envPath))
            {
                Console.WriteLine("[⚠️] .env dosyası bulunamadı.");
                return;
            }

            var lines = File.ReadAllLines(envPath);

            foreach (var line in lines)
            {
                if (string.IsNullOrWhiteSpace(line) || line.TrimStart().StartsWith("#"))
                    continue;

                var parts = line.Split('=', 2);
                if (parts.Length == 2)
                {
                    var key = parts[0].Trim();
                    var value = parts[1].Trim().Trim('"'); // Tırnak varsa sil
                    envValues[key] = value;
                }
            }

            //Console.WriteLine("[✅] .env dosyası yüklendi.");
            //MessageBox.Show("[✅] .env dosyası yüklendi.", "Başarılı", MessageBoxButtons.OK, MessageBoxIcon.Information);

        }

        public static string Get(string key)
        {
            if (envValues.ContainsKey(key))
            {
                return envValues[key]?.Trim();
            }

            Console.WriteLine($"[❌] .env içinde '{key}' bulunamadı.");
            return null;
        }
    }
}

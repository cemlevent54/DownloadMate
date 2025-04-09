using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace downloadmate.helper
{
    public class AppSettings
    {
        public string Theme { get; set; } = "Light";
        public string Language { get; set; } = "tr";
    }

    public static class SettingsManager
    {
        private static string settingsFile = "AppSettings.json";

        public static AppSettings Load()
        {
            if (!File.Exists(settingsFile))
                return new AppSettings();

            try
            {
                var json = File.ReadAllText(settingsFile);
                return JsonSerializer.Deserialize<AppSettings>(json) ?? new AppSettings();
            }
            catch
            {
                return new AppSettings();
            }
        }

        public static void Save(AppSettings settings)
        {
            var json = JsonSerializer.Serialize(settings, new JsonSerializerOptions
            {
                WriteIndented = true
            });

            File.WriteAllText(settingsFile, json);
        }
    }
}

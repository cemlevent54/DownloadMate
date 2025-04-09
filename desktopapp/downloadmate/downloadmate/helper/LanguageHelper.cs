using System.Globalization;
using System.Resources;
using System.Threading;

namespace downloadmate.helper
{
    public static class LanguageHelper
    {
        // ResourceManager, Resources.Strings'den alınmalı çünkü resx dosyasının adı "Strings"
        private static ResourceManager resourceManager = downloadmate.Resources.Strings.ResourceManager;

        public static void SetLanguage(string languageCode)
        {
            if (string.IsNullOrWhiteSpace(languageCode))
                languageCode = "tr"; // Varsayılan Türkçe

            var culture = new CultureInfo(languageCode);
            Thread.CurrentThread.CurrentUICulture = culture;
            Thread.CurrentThread.CurrentCulture = culture;
        }

        public static string GetString(string key)
        {
            return resourceManager.GetString(key) ?? $"[{key}]";
        }
    }
}

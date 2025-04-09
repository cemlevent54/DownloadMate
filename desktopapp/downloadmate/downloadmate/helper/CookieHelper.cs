using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace downloadmate.helper
{
    public static class CookieHelper
    {
        private static readonly string[] RequiredYoutubeCookies = new[]
        {
            "SID", "SAPISID", "HSID", "SSID", "APISID"
        };

        public static string FilterYoutubeCookies(string rawCookies)
        {
            var cookieParts = rawCookies.Split(';');

            var filtered = cookieParts
                .Select(p => p.Trim())
                .Where(p => RequiredYoutubeCookies.Any(req => p.StartsWith(req + "=", StringComparison.OrdinalIgnoreCase)))
                .ToList();

            // Eksik çerez varsa uyarı
            var foundKeys = filtered.Select(p => p.Split('=')[0]).ToList();
            var missing = RequiredYoutubeCookies.Except(foundKeys);

            if (missing.Any())
            {
                System.Windows.Forms.MessageBox.Show("⚠️ Eksik çerez(ler) tespit edildi:\n" + string.Join(", ", missing), "Uyarı");
            }

            return string.Join("; ", filtered);
        }

        public static string FilterInstagramCookies(string rawCookies)
        {
            var required = new[] { "sessionid", "ds_user_id" };
            var parts = rawCookies.Split(';');

            var filtered = parts
                .Select(p => p.Trim())
                .Where(p => required.Any(key => p.StartsWith(key + "=", StringComparison.OrdinalIgnoreCase)))
                .ToList();

            var found = filtered.Select(p => p.Split('=')[0]).ToList();
            var missing = required.Except(found);

            if (missing.Any())
            {
                MessageBox.Show("⚠️ Eksik Instagram çerezi:\n" + string.Join(", ", missing));
            }

            return string.Join("; ", filtered);
        }
    }
}

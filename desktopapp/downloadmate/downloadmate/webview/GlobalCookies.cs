﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace downloadmate.webview
{
    public static class GlobalCookies
    {
        private static string youtubeCookiePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "cookies", "cookies_youtube.txt");

        public static void SaveYouTubeCookies(string cookieString)
        {
            Directory.CreateDirectory(Path.GetDirectoryName(youtubeCookiePath));
            File.WriteAllText(youtubeCookiePath, cookieString);
        }

        public static string? LoadYouTubeCookies()
        {
            if (File.Exists(youtubeCookiePath))
            {
                return File.ReadAllText(youtubeCookiePath);
            }
            return null;
        }

        private static string instagramCookiePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "cookies", "cookies_instagram.txt");

        public static void SaveInstagramCookies(string cookieString)
        {
            Directory.CreateDirectory(Path.GetDirectoryName(instagramCookiePath));
            File.WriteAllText(instagramCookiePath, cookieString);
        }

        public static string? LoadInstagramCookies()
        {
            return File.Exists(instagramCookiePath) ? File.ReadAllText(instagramCookiePath) : null;
        }
    }
}

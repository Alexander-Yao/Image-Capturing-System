using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MapsVisionsAPI.Middleware
{
    public class FuzzyText
    {
        public static int TextDistance(string src, string dest)
        {
            if (src.Trim() == dest.Trim())
                return 0;
            int[,] d = new int[src.Length + 1, dest.Length + 1];
            int i, j, cost;
            char[] str1 = src.ToCharArray();
            char[] str2 = dest.ToCharArray();

            for (i = 0; i <= str1.Length; i++)
            {
                d[i, 0] = i;
            }
            for (j = 0; j <= str2.Length; j++)
            {
                d[0, j] = j;
            }
            for (i = 1; i <= str1.Length; i++)
            {
                for (j = 1; j <= str2.Length; j++)
                {

                    if (str1[i - 1] == str2[j - 1])
                        cost = 0;
                    else
                        cost = 1;

                    d[i, j] =
                        Math.Min(
                            d[i - 1, j] + 1,              // Deletion
                            Math.Min(
                                d[i, j - 1] + 1,          // Insertion
                                d[i - 1, j - 1] + cost)); // Substitution

                    if ((i > 1) && (j > 1) && (str1[i - 1] ==
                        str2[j - 2]) && (str1[i - 2] == str2[j - 1]))
                    {
                        d[i, j] = Math.Min(d[i, j], d[i - 2, j - 2] + cost);
                    }
                }
            }

            return d[str1.Length, str2.Length];
        }
        public static string[,] SearchList(string[] wordsList, string[] CorrectWords, double fuzzyness = 0.5)
        {
            string[,] WordsMatchingDegrees = new string[wordsList.Length, 3];
            for (int x = 0; x > wordsList.Length; x++)
            {
                //try
                //{
                var res = FindMatchingDegree(wordsList[x], CorrectWords, fuzzyness);
                WordsMatchingDegrees[x, 0] = wordsList[x];
                WordsMatchingDegrees[x, 1] = res[0, 0];
                WordsMatchingDegrees[x, 2] = res[0, 1];
                /*}
                catch (Exception)
                {
                    WordsMatchingDegrees[x, 0] = wordsList[x];
                    WordsMatchingDegrees[x, 1] = "";
                    WordsMatchingDegrees[x, 2] = "0.0";
                }*/
            }
            return WordsMatchingDegrees;
        }
        public static string[,] FindMatchingDegree(string word, string[] wordList, double fuzzyness)
        {

            string[,] foundWords = new string[wordList.Length, 2];

            for (int x = 0; x < wordList.Length; x++) // (string s in wordList)
            {
                // Response.Write("wordList[x]=" + wordList[x]);
                string ComparativeWord = wordList[x];
                //  Response.Write("ComparativeWord="+ ComparativeWord);
                // Calculate the word-distance:
                int textDistance =
                    TextDistance(word.Trim(), ComparativeWord.Trim());
                // Response.Write("textDistance="+textDistance);
                // Length of the longer string:
                int length = Math.Max(word.Trim().Length, ComparativeWord.Trim().Length);

                // Calculate the score:
                double score = 1.0 - (double)textDistance / length;
                // Match?
                if (score > fuzzyness)
                {
                    foundWords[x, 0] = ComparativeWord.Trim();
                    foundWords[x, 1] = String.Format("{0:0.00}", score);
                }
            }

            return getMaxMatching(foundWords);
        }

        private static string[,] getMaxMatching(string[,] foundWords)
        {
            double max = 0.0;
            string word = "";
            for (int x = 0; x < foundWords.Length; x++)
                try
                {
                    if (max < double.Parse(foundWords[x, 1]))
                    {
                        max = double.Parse(foundWords[x, 1]);
                        word = foundWords[x, 0];
                    }
                }
                catch (Exception)
                {
                    ;
                }

            return new string[,] { { word, max.ToString() } };
        }
    }
}

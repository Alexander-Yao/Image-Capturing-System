using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace MapsVisionsAPI.Middleware
{
    public class TextProcessing
    {
        public static List<string[]> CastCSVToDataTable(StringReader reader)
        {
            string line = "";
            List<string[]> datatable = new List<string[]>();
            while ((line = reader.ReadLine()) != null)
            {
                string[] rowData = line.Split('\t');

                if (rowData[rowData.Length - 1].Trim().Length > 0)
                    datatable.Add(rowData);
            }
            return datatable;
        }
        public static string[] castLinedTextToStringArray(string allText)
        {
            return allText.Split("\n").Where(ele => ele.Trim() != "").ToArray();
        }
        public static Dictionary<string, string> getTableOfUndetectedWords(string[] CorrectWords, List<string[]> tableOfWordsResult)
        {
            Dictionary<string, string> undetectedTable = new Dictionary<string, string>();
            for (int x = 0; x < CorrectWords.Length; x++)
            {
                bool exists = false;
                for (int row = 0; row < tableOfWordsResult.Count; row++)
                {
                    string[] line = tableOfWordsResult[row];

                    string CWordTable = line[12].ToString();
                    if (CWordTable.Trim().Length > 0)
                        if (CorrectWords[x].Trim().Contains(CWordTable))
                        {
                            exists = true;
                            continue;
                        }
                }
                if (!exists)
                {
                    undetectedTable.Add(CorrectWords[x], "0");
                }

            }
            return undetectedTable;
        }
        public static List<string[]> getTableWithMatchingDegree(List<string[]> tableOfWordsResult, string[] correctWords, 
                                out int wrongWords, out int countMatchingDegreeRows, out float sumMatchingDegree)
        {
            List<string[]> tableOfWordsResultWithMatchingDegree = new List<string[]>();
            wrongWords = 0;
            countMatchingDegreeRows = 0;
            sumMatchingDegree = 0;
            int lineno = 0;

            foreach (var line in tableOfWordsResult)
            {
                string[] rowData = line;

                System.Array.Resize<string>(ref rowData, 14);

                if (rowData[11].Trim().Length > 0)
                {
                    var res = FuzzyText.FindMatchingDegree(rowData[11].ToString(), correctWords, 0.4);

                    rowData[12] = res[0, 0]; //Correct Word
                    rowData[13] = res[0, 1]; //Matching Degree

                    if (rowData[13].ToString() == "0")
                        wrongWords += 1;
                    else
                    {
                        countMatchingDegreeRows += 1;
                        float convfloat = 0;
                        if (!float.TryParse(rowData[13].ToString(), out convfloat))
                            throw new FormatException("I can't convert value of=" + rowData[13].ToString());
                        else
                            sumMatchingDegree += convfloat;
                        tableOfWordsResultWithMatchingDegree.Add(rowData);
                    }
                    lineno += 1;

                }

            }
            return tableOfWordsResultWithMatchingDegree;
        }
    }
}

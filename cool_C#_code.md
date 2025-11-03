мной было потрачено много времени у умственного ресурса, чтобы написать этот код, но зато теперь я разобрался в этих сраных словарях.
```C#
namespace TextAnalysis;

static class FrequencyAnalysisTask
{
    public static void GramCount(Dictionary<string, Dictionary<string, int>> timeDic, string key, string dict)
    {
        if (!timeDic.ContainsKey(key))
        {
            timeDic[key] = new Dictionary<string, int>();
        }
        if (!timeDic[key].ContainsKey(dict))
        {
            timeDic[key][dict] = 0;
        }
        timeDic[key][dict]++;
	}

    public static Dictionary<string, string> ClearBib(Dictionary<string, Dictionary<string, int>> timeDic)
    {
        var dict = new Dictionary<string, string>();
        foreach (var key in timeDic.Keys)
		{
			var bestkey = "";
        	var keyNum = 0;
            foreach (var val in timeDic[key].Keys)
            {
                if (keyNum != 0 && timeDic[key][val] == keyNum)
                {
                    if (string.CompareOrdinal(val, bestkey) < 0)
                    {
                        bestkey = val;
                    }
                }
                if (timeDic[key][val] > keyNum)
                {
                    keyNum = timeDic[key][val];
                    bestkey = val;
                }
			}
			dict[key] = bestkey;
        }
        return dict;
	}

    public static Dictionary<string, string> GetMostFrequentNextWords(List<List<string>> text)
    {
        var timeDic = new Dictionary<string, Dictionary<string, int>>();

        foreach (var sentece in text)
        {
            for (int i = 0; i < sentece.Count - 1; i++)
            {
                GramCount(timeDic, sentece[i], sentece[i + 1]);
            }
            for (int i = 0; i < sentece.Count - 2; i++)
            {
                string key = sentece[i] + " " + sentece[i + 1];
                GramCount(timeDic, key, sentece[i + 2]);
            }
        }
        return ClearBib(timeDic);
    }
}

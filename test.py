import matplotlib.pyplot as plt

import pandas as pd
import csv



from pysentimiento import create_analyzer

analyzer = create_analyzer(task="sentiment", lang="en")
result = analyzer.predict("I love this app!")
print(result)

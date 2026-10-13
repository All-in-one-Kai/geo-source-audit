"""Print synthetic output, never call an engine or write an audit history."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from geo_source_audit import report
project={'label':'SYNTHETIC OFFLINE EXAMPLE — not a market measurement','own_domains':['example.com'],'own_names':['Demo Brand']}
rows=[{'question':'Synthetic buyer question','engine':'offline fixture','named':True,'cited':True,'domains':['example.com','other.test']}]
print(report('demo',project,rows,[],{})[0])

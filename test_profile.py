import tempfile
import unittest
from pathlib import Path
from inspect_bog import profile_csv


class ProfileTests(unittest.TestCase):
    def test_missing_and_invalid_values_are_not_converted_to_zero(self):
        header = 'Mnemonic,Parent Mnemonic,Name of Series,Data Family,Units of Measure,a,b,c,d,Jan-26,Feb-26,Mar-26,Apr-26\n'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'input.csv'
            path.write_text(header + 'X,,Example,Prices,index,,,,,0,,NaN,"1,200"\n')
            row = profile_csv(path)[0]
        self.assertEqual(row['values'], {'Jan-26': 0.0, 'Apr-26': 1200.0})
        self.assertEqual(row['zeros'], 1)
        self.assertEqual(row['bad'], [('Mar-26', 'NaN')])


if __name__ == '__main__':
    unittest.main()

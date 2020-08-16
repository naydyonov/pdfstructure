from collections import Counter
from pathlib import Path
from unittest import TestCase

from pdfstructure.style_analyser import TextSize, PivotLinearMapper, PivotLogMapper
from pdfstructure.style_analyser import count_sizes, StyleDistribution
from pdfstructure.title_finder import DocumentTitleExtractor
from utils import element_generator


class TestSizeMapper(TestCase):
    
    def test_log_mapper(self):
        distribution = StyleDistribution(Counter((1, 5, 6, 10, 10, 10, 10, 20, 100)))
        scaler = PivotLogMapper(distribution)
        # test borders
        borders = (5.50, 8.58, 17.08, 32.48)
        [self.assertAlmostEqual(borders[i], b, 2) for i, b in enumerate(scaler.borders)]
        self.assertEqual(TextSize.xsmall, scaler.translate(TextSize, -10))
        self.assertEqual(TextSize.xsmall, scaler.translate(TextSize, 0))
        self.assertEqual(TextSize.xsmall, scaler.translate(TextSize, 1))
        self.assertEqual(TextSize.xsmall, scaler.translate(TextSize, 5))
        self.assertEqual(TextSize.small, scaler.translate(TextSize, 6))
        self.assertEqual(TextSize.small, scaler.translate(TextSize, 7))
        self.assertEqual(TextSize.small, scaler.translate(TextSize, 8))
        self.assertEqual(TextSize.middle, scaler.translate(TextSize, 9))
        self.assertEqual(TextSize.middle, scaler.translate(TextSize, 10))
        self.assertEqual(TextSize.middle, scaler.translate(TextSize, 15))
        self.assertEqual(TextSize.middle, scaler.translate(TextSize, 17))
        self.assertEqual(TextSize.large, scaler.translate(TextSize, 18))
        self.assertEqual(TextSize.large, scaler.translate(TextSize, 30))
        self.assertEqual(TextSize.xlarge, scaler.translate(TextSize, 40))
        self.assertEqual(TextSize.xlarge, scaler.translate(TextSize, 50))
        self.assertEqual(TextSize.xlarge, scaler.translate(TextSize, 60))
        self.assertEqual(TextSize.xlarge, scaler.translate(TextSize, 70))
        self.assertEqual(TextSize.xlarge, scaler.translate(TextSize, 90))
        self.assertEqual(TextSize.xlarge, scaler.translate(TextSize, 120))
    
    def test_linear_mapper(self):
        distribution = StyleDistribution(Counter((1, 5, 6, 10, 10, 10, 10, 20, 100)))
        scaler = PivotLinearMapper(distribution)
        
        self.assertTupleEqual((3.25, 5.5, 32.5, 55.0), scaler.borders)
        
        self.assertEqual(TextSize.xsmall, scaler.translate(TextSize, -10))
        self.assertEqual(TextSize.xsmall, scaler.translate(TextSize, 0))
        self.assertEqual(TextSize.xsmall, scaler.translate(TextSize, 1))
        self.assertEqual(TextSize.small, scaler.translate(TextSize, 5))
        self.assertEqual(TextSize.middle, scaler.translate(TextSize, 10))
        self.assertEqual(TextSize.middle, scaler.translate(TextSize, 15))
        self.assertEqual(TextSize.middle, scaler.translate(TextSize, 20))
        self.assertEqual(TextSize.middle, scaler.translate(TextSize, 30))
        self.assertEqual(TextSize.large, scaler.translate(TextSize, 40))
        self.assertEqual(TextSize.large, scaler.translate(TextSize, 50))
        self.assertEqual(TextSize.xlarge, scaler.translate(TextSize, 60))
        self.assertEqual(TextSize.xlarge, scaler.translate(TextSize, 70))
        self.assertEqual(TextSize.xlarge, scaler.translate(TextSize, 90))
        self.assertEqual(TextSize.xlarge, scaler.translate(TextSize, 120))


class TestStyleAnalyser(TestCase):
    test_path_1 = str(Path("resources/interview_cheatsheet.pdf").absolute())
    test_path_2 = str(Path("resources/IE00BM67HT60-ATB-FS-DE-2020-2-28.pdf").absolute())
    test_ppt = str(Path("resources/samplepptx.pdf").absolute())
    
    def test_title_extraction_sample_ppt(self):
        element_gen = element_generator(self.test_ppt)
        distribution = count_sizes(element_gen)
        self.assertFalse(distribution.is_empty)
        self.assertAlmostEqual(32, distribution.body_size, delta=0.1)
        self.assertAlmostEqual(32, distribution.min_found_size, delta=0.1)
        self.assertAlmostEqual(44, distribution.max_found_size, delta=0.1)
        self.assertEqual(2, distribution.amount_sizes)
        extractor = DocumentTitleExtractor()
        title = extractor.process(distribution, elements=element_generator(self.test_ppt))
        self.assertEqual('Sample_PowerPoint_File__This_is_a_Sample_Slide', title)
    
    def test_title_extraction_tech_cheatsheet(self):
        element_gen = element_generator(self.test_path_1)
        distribution = count_sizes(element_gen)
        self.assertFalse(distribution.is_empty)
        self.assertAlmostEqual(6.4, distribution.min_found_size, delta=0.1)
        self.assertAlmostEqual(8.5, distribution.body_size, delta=0.1)
        self.assertEqual(8, distribution.amount_sizes)
        
        extractor = DocumentTitleExtractor()
        title = extractor.process(distribution, elements=element_generator(self.test_path_1))
        self.assertEqual("TSiege_The_Technical_Interview_Cheat_Sheet.md__ANNOUNCEMENT__"
                         "Studying_for_a_Tech_Interview_Sucks,_so_Here's_a_Cheat_Sheet_to_Help__Array", title)
    
    def test_title_extraction_msci_world(self):
        element_gen = element_generator(self.test_path_2)
        distribution = count_sizes(element_gen)
        self.assertFalse(distribution.is_empty)
        self.assertAlmostEqual(6, distribution.body_size, delta=0.1)
        self.assertEqual(7, distribution.amount_sizes)
        
        extractor = DocumentTitleExtractor()
        title = extractor.process(distribution, elements=element_generator(self.test_path_2))
        self.assertEqual('Xtrackers_MSCI_World_Information_Technology_UCITS_ETF_1C', title)
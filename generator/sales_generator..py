# -*- coding: utf-8 -*-
"""
Dataset Generator - Python 2.7 Compatible
"""
import random
import time
from datetime import datetime, timedelta
import sys
import os

# For Python 2/3 compatibility
try:
    from itertools import izip as zip
    range = xrange  # Use xrange for memory efficiency
except ImportError:
    pass

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("Warning: numpy not installed, using random module for distributions")

class EfficientDatasetGeneratorPy2:
    """Python 2.7 compatible dataset generator"""
    
    def __init__(self):
        # ============================================
        # CONFIGURATION - CITIES WITH WEIGHTS
        # ============================================
        self.cities_data = [
            ('A Corunha', 1.5), ('Vigo', 1.5), ('Santiago', 1.3),
            ('Ourense', 1.2), ('Lugo', 1.2), ('Pontevedra', 1.2),
            ('Ferrol', 1.0), ('Naron', 1.0), ('Oleiros', 1.0),
            ('Carballo', 1.0), ('Arteixo', 1.0), ('Ribeira', 1.0),
            ('Cangas', 0.8), ('Marin', 0.8), ('Burela', 0.7),
            ('Sarria', 0.7), ('Monforte', 0.6), ('Chantada', 0.6),
            ('Foz', 0.5), ('Mondonhedo', 0.5)
        ]
        
        self.cities = [c[0] for c in self.cities_data]
        self.city_weights = [c[1] for c in self.cities_data]
        
        # ============================================
        # CATEGORIES WITH PRICE RANGES
        # ============================================
        self.categories = {
            'Alimentacion': (1.0, 50.0),
            'Electronica': (100.0, 3000.0),
            'Ropa': (15.0, 400.0),
            'Hogar': (10.0, 600.0),
            'Juguetes': (8.0, 200.0),
            'Deportes': (20.0, 500.0),
            'Libros': (8.0, 80.0),
            'Musica': (10.0, 120.0),
            'Cine': (5.0, 20.0),
            'Jardineria': (3.0, 250.0),
            'Ferreteria': (2.0, 350.0),
            'Cosmetica': (8.0, 300.0),
            'Farmacia': (5.0, 120.0),
            'Automocion': (20.0, 1000.0),
            'Mascotas': (6.0, 180.0),
            'Moda hombre': (25.0, 450.0),
            'Moda mujer': (25.0, 550.0),
            'Calzado': (30.0, 350.0),
            'Complementos': (8.0, 250.0),
            'Bebes': (12.0, 400.0)
        }
        
        self.category_list = self.categories.keys()
        
        # ============================================
        # TIME DISTRIBUTION (9:00 - 20:00)
        # ============================================
        # Hours with weights (9-20)
        self.hour_weights = [
            0.06,  # 9
            0.08,  # 10
            0.10,  # 11
            0.15,  # 12 - PEAK 1
            0.09,  # 13
            0.05,  # 14
            0.04,  # 15
            0.06,  # 16
            0.10,  # 17
            0.16,  # 18 - PEAK 2
            0.08,  # 19
            0.03   # 20
        ]
        self.hours = range(9, 21)  # 9 to 20 inclusive
        
        # ============================================
        # PAYMENT METHODS LOGIC
        # ============================================
        self.payment_methods = [
            'cash', 'visa', 'mastercard', 'transferencia', 
            'bizum', 'paypal', 'cheque', 'efectivo', 'tarjeta regalo'
        ]
        
        # Price thresholds for payment methods
        self.LOW_PRICE_THRESHOLD = 50.0
        self.HIGH_PRICE_THRESHOLD = 300.0
        
        # Initialize random seed
        random.seed(time.time())
    
    def weighted_choice(self, choices, weights):
        """Python 2 compatible weighted random choice"""
        total = sum(weights)
        r = random.uniform(0, total)
        upto = 0
        for c, w in zip(choices, weights):
            if upto + w >= r:
                return c
            upto += w
        return choices[-1]
    
    def generate_city(self):
        """Generate city based on weights"""
        return self.weighted_choice(self.cities, self.city_weights)
    
    def generate_hour(self):
        """Generate hour based on time distribution"""
        return self.weighted_choice(self.hours, self.hour_weights)
    
    def generate_price(self, category):
        """Generate price for a given category"""
        low, high = self.categories[category]
        
        # 70% low prices, 30% high prices
        if random.random() < 0.7:
            # Lower third of price range
            price = random.uniform(low, low + (high - low) * 0.33)
        else:
            # Upper two-thirds
            price = random.uniform(low + (high - low) * 0.33, high)
        
        # Add some noise and round
        price *= random.uniform(0.95, 1.05)
        return round(price, 2)
    
    def generate_payment_method(self, price):
        """Generate payment method based on price"""
        if price < self.LOW_PRICE_THRESHOLD:
            # Low price: cash is king
            methods = ['cash', 'efectivo', 'bizum', 'visa', 'mastercard']
            weights = [0.40, 0.30, 0.15, 0.10, 0.05]
        elif price > self.HIGH_PRICE_THRESHOLD:
            # High price: bank transfers and cards
            methods = ['transferencia', 'visa', 'mastercard', 'paypal', 'cheque']
            weights = [0.35, 0.25, 0.20, 0.10, 0.10]
        else:
            # Medium price: mix
            methods = ['visa', 'mastercard', 'metalico', 'efectivo', 'bizum']
            weights = [0.25, 0.20, 0.15, 0.15, 0.10]
        
        return self.weighted_choice(methods, weights)
    
    def generate_datetime(self, start_date, end_date):
        """Generate random datetime between two dates"""
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        delta_days = (end - start).days
        random_days = random.randint(0, delta_days)
        
        random_date = start + timedelta(days=random_days)
        random_hour = self.generate_hour()
        random_minute = random.randint(0, 59)
        
        return random_date.replace(hour=random_hour, minute=random_minute)
    
    def generate_row(self, start_date, end_date):
        """Generate a single row as a tab-separated string"""
        dt = self.generate_datetime(start_date, end_date)
        city = self.generate_city()
        category = random.choice(self.category_list)
        price = self.generate_price(category)
        payment = self.generate_payment_method(price)
        
        # Format: YYYY-MM-DD HH:MM\tCity\tCategory\tPrice\tPayment
        return "%s\t%s\t%s\t%s\t%s" % (
            dt.strftime('%Y-%m-%d %H:%M'),
            city,
            category,
            price,
            payment
        )
    
    def generate_to_file(self, num_rows, 
                        start_date='2020-01-01',
                        end_date='2023-12-31',
                        filename='sales_dataset.csv',
                        batch_size=100000):
        """
        Generate dataset directly to file with memory-efficient batching
        
        Args:
            num_rows: Total number of rows to generate
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            filename: Output filename
            batch_size: Rows to write in each batch (for memory efficiency)
        """
        print("Generating {:,} rows...".format(num_rows))
        print("Date range: {} to {}".format(start_date, end_date))
        print("Output file: {}".format(filename))
        
        start_time = time.time()
        
        # Open file for writing
        f = open(filename, 'w')
        
        # Write header
        #f.write("fecha_hora\tciudad\tcategoria\tprecio\ttipo_pago\n")
        
        # Write data in batches
        batches = (num_rows + batch_size - 1) // batch_size
        
        for batch_num in range(batches):
            batch_start = batch_num * batch_size
            batch_end = min(batch_start + batch_size, num_rows)
            batch_size_actual = batch_end - batch_start
            
            # Generate and write batch
            batch_rows = []
            for _ in range(batch_size_actual):
                batch_rows.append(self.generate_row(start_date, end_date))
            
            f.write('\n'.join(batch_rows))
            if batch_end < num_rows:
                f.write('\n')  # Add newline except for last batch
            
            # Progress reporting
            if (batch_num + 1) % max(1, batches // 20) == 0 or batch_num == batches - 1:
                elapsed = time.time() - start_time
                rows_per_sec = batch_end / elapsed if elapsed > 0 else 0
                print("  Progress: {:,}/{:,} rows ({:.1f}%) - {:.0f} rows/sec".format(
                    batch_end, num_rows, batch_end/float(num_rows)*100, rows_per_sec))
        
        f.close()
        
        elapsed_time = time.time() - start_time
        print("\nGeneration complete!")
        print("Total time: {:.2f} seconds".format(elapsed_time))
        print("Average speed: {:.0f} rows/second".format(num_rows/elapsed_time))
        
        # Calculate file size
        file_size = os.path.getsize(filename)
        file_size_mb = file_size / 1024.0 / 1024.0
        if file_size_mb > 1024:
            file_size_gb = file_size_mb / 1024.0
            print("File size: {:.2f} MB ({:.2f} GB)".format(file_size_mb, file_size_gb))
        else:
            print("File size: {:.2f} MB".format(file_size_mb))
    
    def generate_sample_statistics(self, sample_size=10000,
                                 start_date='2020-01-01',
                                 end_date='2023-12-31'):
        """
        Generate a small sample and show statistics
        """
        print("Generating sample for statistics verification...")
        
        from collections import defaultdict
        import math
        
        city_counter = defaultdict(int)
        category_counter = defaultdict(int)
        payment_counter = defaultdict(int)
        hour_counter = defaultdict(int)
        prices_by_payment = defaultdict(list)
        
        for _ in range(sample_size):
            dt = self.generate_datetime(start_date, end_date)
            city = self.generate_city()
            category = random.choice(self.category_list)
            price = self.generate_price(category)
            payment = self.generate_payment_method(price)
            
            city_counter[city] += 1
            category_counter[category] += 1
            payment_counter[payment] += 1
            hour_counter[dt.hour] += 1
            prices_by_payment[payment].append(price)
        
        print("\n" + "="*60)
        print("SAMPLE STATISTICS ({:,} rows)".format(sample_size))
        print("="*60)
        
        # Sort counters
        def sort_dict_by_value(d, reverse=True):
            return sorted(d.items(), key=lambda x: x[1], reverse=reverse)
        
        print("\nTop 5 Cities:")
        for city, count in sort_dict_by_value(city_counter)[:5]:
            print("  {}: {} ({:.1f}%)".format(city, count, count/float(sample_size)*100))
        
        print("\nTop 5 Categories:")
        for cat, count in sort_dict_by_value(category_counter)[:5]:
            print("  {}: {} ({:.1f}%)".format(cat, count, count/float(sample_size)*100))
        
        print("\nPayment Methods:")
        for payment, count in sort_dict_by_value(payment_counter):
            if prices_by_payment[payment]:
                avg_price = sum(prices_by_payment[payment]) / len(prices_by_payment[payment])
            else:
                avg_price = 0
            print("  {}: {} ({:.1f}%), avg price: €{:.2f}".format(
                payment, count, count/float(sample_size)*100, avg_price))
        
        print("\nHour Distribution (9-20):")
        for hour in sorted(hour_counter.keys()):
            if 9 <= hour <= 20:
                count = hour_counter[hour]
                print("  {:02d}:00: {} ({:.1f}%)".format(
                    hour, count, count/float(sample_size)*100))
        
        print("\nPeak Hours Check:")
        print("  12:00: {} ({:.1f}%)".format(
            hour_counter.get(12, 0), 
            hour_counter.get(12, 0)/float(sample_size)*100))
        print("  18:00: {} ({:.1f}%)".format(
            hour_counter.get(18, 0), 
            hour_counter.get(18, 0)/float(sample_size)*100))


# ============================================================================
# SIMPLIFIED VERSION - NO EXTERNAL DEPENDENCIES
# ============================================================================

class SimpleDatasetGeneratorPy2:
    """Simplest Python 2.7 version with no dependencies"""
    
    def __init__(self):
        # Fixed lists - no weights for simplicity
        self.cities = [
            'A Corunha', 'Vigo', 'Santiago', 'Ourense', 'Lugo',
            'Pontevedra', 'Ferrol', 'Naron', 'Oleiros', 'Carballo'
        ]
        
        self.categories = [
            'Alimentacion', 'Electronica', 'Ropa', 'Hogar', 'Deportes'
        ]
        
        self.payment_methods = [
            'cash', 'visa', 'mastercard', 'transferencia', 'bizum'
        ]
        
        # Price ranges by category
        self.price_ranges = {
            'Alimentacion': (1, 50),
            'Electronica': (100, 2000),
            'Ropa': (15, 300),
            'Hogar': (10, 500),
            'Deportes': (20, 400)
        }
    
    def generate_datetime_str(self, year=2023):
        """Generate datetime string directly"""
        # Random day of year
        day_of_year = random.randint(1, 365)
        date = datetime(year, 1, 1) + timedelta(days=day_of_year - 1)
        
        # Hours: peak at 12 and 18
        hour_weights = [6, 8, 10, 15, 9, 5, 4, 6, 10, 16, 8, 3]
        hour = 9
        r = random.randint(1, 100)
        cumulative = 0
        for i, weight in enumerate(hour_weights):
            cumulative += weight
            if r <= cumulative:
                hour = 9 + i
                break
        
        minute = random.randint(0, 59)
        
        return date.replace(hour=hour, minute=minute).strftime('%Y-%m-%d %H:%M')
    
    def generate_price(self, category):
        """Generate price based on category"""
        low, high = self.price_ranges.get(category, (1, 100))
        
        # Simple distribution: 70% low, 30% high
        if random.random() < 0.7:
            return round(random.uniform(low, low + (high - low) * 0.3), 2)
        else:
            return round(random.uniform(low + (high - low) * 0.3, high), 2)
    
    def generate_payment(self, price):
        """Generate payment method based on price"""
        if price < 50:
            # Cash for small amounts
            if random.random() < 0.7:
                return 'metálico'
            else:
                return random.choice(['bizum', 'visa'])
        elif price > 300:
            # Transfer for large amounts
            if random.random() < 0.6:
                return 'transferencia'
            else:
                return random.choice(['visa', 'mastercard'])
        else:
            # Mixed for medium amounts
            return random.choice(self.payment_methods)
    
    def generate_simple_file(self, num_rows, filename='simple_sales.txt'):
        """Generate file in one pass - simplest version"""
        print("Generating {:,} rows to {}...".format(num_rows, filename))
        
        start_time = time.time()
        
        with open(filename, 'w') as f:
            # Write header
            #f.write("fecha_hora\tciudad\tcategoria\tprecio\ttipo_pago\n")
            
            # Write rows
            for i in range(num_rows):
                # Generate data
                dt_str = self.generate_datetime_str()
                city = random.choice(self.cities)
                category = random.choice(self.categories)
                price = self.generate_price(category)
                payment = self.generate_payment(price)
                
                # Write row
                f.write("%s\t%s\t%s\t%s\t%s\n" % (dt_str, city, category, price, payment))
                
                # Progress every 10%
                if (i + 1) % (num_rows // 10) == 0:
                    elapsed = time.time() - start_time
                    rows_per_sec = (i + 1) / elapsed if elapsed > 0 else 0
                    print("  {:,}/{:,} ({:.0f}%) - {:.0f} rows/sec".format(
                        i + 1, num_rows, (i + 1)/float(num_rows)*100, rows_per_sec))
        
        elapsed = time.time() - start_time
        print("\nDone! {:.2f} seconds, {:.0f} rows/sec".format(elapsed, num_rows/elapsed))
        
        # Show file size
        size = os.path.getsize(filename)
        print("File size: {:.1f} MB".format(size / 1024.0 / 1024.0))


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function - choose which generator to use"""
    
    print("="*60)
    print("PYTHON 2.7 DATASET GENERATOR")
    print("="*60)
    print("\nChoose an option:")
    print("1. Full-featured generator (recommended)")
    print("2. Simple generator (no dependencies)")
    print("3. Test with small dataset")
    
    choice = raw_input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        # Option 1: Full-featured generator
        print("\n" + "="*60)
        print("FULL-FEATURED GENERATOR")
        print("="*60)
        
        gen = EfficientDatasetGeneratorPy2()
        
        # Show sample statistics first
        gen.generate_sample_statistics(sample_size=5000)
        
        # Ask for parameters
        print("\n" + "-"*60)
        num_rows = int(raw_input("How many rows to generate? (e.g., 1000000): ") or "1000000")
        filename = raw_input("Output filename? (default: sales_data.txt): ") or "sales_data.txt"
        
        print("\nGenerating {:,} rows...".format(num_rows))
        gen.generate_to_file(
            num_rows=num_rows,
            filename=filename,
            batch_size=50000
        )
        
    elif choice == "2":
        # Option 2: Simple generator
        print("\n" + "="*60)
        print("SIMPLE GENERATOR")
        print("="*60)
        
        gen = SimpleDatasetGeneratorPy2()
        
        num_rows = int(raw_input("How many rows to generate? (e.g., 100000): ") or "100000")
        filename = raw_input("Output filename? (default: simple_sales.txt): ") or "simple_sales.txt"
        
        gen.generate_simple_file(num_rows=num_rows, filename=filename)
        
    elif choice == "3":
        # Option 3: Test with small dataset
        print("\n" + "="*60)
        print("TEST GENERATION (10,000 rows)")
        print("="*60)
        
        gen = EfficientDatasetGeneratorPy2()
        gen.generate_sample_statistics(sample_size=10000)
        
        # Generate small file
        gen.generate_to_file(
            num_rows=10000,
            filename='test_output.txt',
            batch_size=1000
        )
        
        print("\nTest file generated: test_output.txt")
        print("First 5 lines:")
        print("-" * 60)
        with open('test_output.txt', 'r') as f:
            for i in range(6):  # Header + 5 rows
                print(f.readline().strip())
    
    else:
        print("Invalid choice. Using default...")
        
        # Default: generate 100,000 rows
        gen = SimpleDatasetGeneratorPy2()
        gen.generate_simple_file(num_rows=100000, filename='default_output.txt')


def quick_start():
    """Quick start - just run with defaults"""
    print("Quick generation of 100,000 rows...")
    
    # Use simple generator for maximum compatibility
    gen = SimpleDatasetGeneratorPy2()
    gen.generate_simple_file(num_rows=100000, filename='sales_100k.txt')
    
    print("\nDone! File saved as 'sales_100k.txt'")


# Run the script
if __name__ == "__main__":
    try:
        # For quick testing, uncomment:
        # quick_start()
        
        # For interactive mode:
        main()
        
    except KeyboardInterrupt:
        print("\n\nGeneration cancelled by user.")
    except Exception as e:
        print("\nError: {}".format(e))
        import traceback
        traceback.print_exc()
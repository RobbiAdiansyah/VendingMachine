import time
import os
import sys

class VendingMachineDFA:
    def __init__(self):
        # State awal adalah q0
        self.state = 'q0'
        
        # Mapping State ke Nilai (Definisi State)
        self.state_map = {
            'q0': 0,
            'q1': 5000,
            'q2': 10000,
            'q3': 15000,
            'q4': 20000,
            'q5': 'KELUAR' # State Final
        }
        
        # Mapping Nilai ke State (Untuk mencari state tujuan setelah transaksi)
        # Kita membalik dictionary di atas agar bisa cari key berdasarkan value
        self.val_to_state = {v: k for k, v in self.state_map.items() if k != 'q5'}
        
        # Database Produk
        self.products = {
            "1": {"name": "Air Mineral", "price": 5000},
            "2": {"name": "Teh Botol", "price": 10000},
            "3": {"name": "Susu Kotak", "price": 15000},
            "4": {"name": "Kopi Kaleng", "price": 20000}
        }

    def get_balance(self):
        """Helper untuk mendapatkan nilai uang dari state saat ini"""
        if self.state == 'q5': return 0
        return self.state_map[self.state]

    def display_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear') 
        current_balance = self.get_balance()
        
        print(f"\n{'='*45}")
        # Menampilkan State dan Nilai Aslinya
        print(f"   VENDING MACHINE (DFA)")
        print(f"   CURRENT STATE: [{self.state}] -> Rp {current_balance}")
        print(f"{'='*45}")
        
        print("Daftar Produk:")
        for key, item in self.products.items():
            # Cek logika berdasarkan saldo (value dari state)
            if current_balance >= item['price']:
                status = "[BISA DIBELI]" 
            else:
                status = "(Saldo Kurang)"
            print(f"[{key}] {item['name']} \t: Rp {item['price']} {status}")
            
        print("-" * 45)
        print("Input (Transisi):")
        print("[5]  Masukkan 5.000  (Naik State)")
        print("[10] Masukkan 10.000 (Lompat State)")
        print("[0]  SELESAI / REFUND (Ke State q5)")
        print(f"{'='*45}")

    def transition(self, input_code):
        print(f"\n>> Input diterima: {input_code}")
        time.sleep(0.5)
        
        current_val = self.get_balance()

        # --- LOGIKA TRANSISI KE STATE q5 (KELUAR) ---
        if input_code == '0':
            print(">> Transisi ke State q5 (KELUAR)...")
            # Simpan saldo sebentar untuk refund sebelum ganti state
            refund_amount = current_val
            
            # PINDAH STATE
            self.state = 'q5'
            
            if refund_amount > 0:
                self.refund(refund_amount)
            else:
                print(">> Tidak ada saldo tersisa.")
            
            print("Mesin Berhenti di State q5.")
            sys.exit()

        # --- LOGIKA TRANSISI INPUT UANG ---
        elif input_code in ['5', '10']:
            add_val = 5000 if input_code == '5' else 10000
            target_val = current_val + add_val
            
            # Cek apakah target value ada di daftar state kita (Max 20000/q4)
            if target_val in self.val_to_state:
                # PINDAH STATE
                self.state = self.val_to_state[target_val]
                print(f">> Saldo bertambah. State berubah menjadi {self.state}")
            else:
                # Jika input membuat saldo > 20.000, tolak karena tidak ada statenya (misal q6 tidak ada)
                print(f">> State untuk nilai Rp {target_val} tidak didefinisikan.")
                print(">> Uang dikembalikan (State tetap).")

        # --- LOGIKA TRANSISI BELI BARANG ---
        elif input_code in self.products:
            item = self.products[input_code]
            price = item['price']
            
            if current_val >= price:
                print(f"\n*** MENGELUARKAN {item['name']} ***")
                time.sleep(1)
                
                # Hitung sisa uang untuk menentukan state tujuan
                new_val = current_val - price
                
                # PINDAH STATE (Mundur ke state yang lebih kecil)
                self.state = self.val_to_state[new_val]
                
                print(f">> Transaksi Berhasil.")
                print(f">> State turun menjadi {self.state} (Sisa: Rp {new_val})")
            else:
                print(f">> Gagal. State {self.state} tidak cukup untuk membeli item ini.")
        
        else:
            print(">> Input tidak valid.")
        
        time.sleep(1.5)

    def refund(self, amount):
        print(f"*** REFUND: Mengeluarkan uang Rp {amount} ***")

# --- MAIN PROGRAM ---
def run():
    vm = VendingMachineDFA()
    
    while True:
        vm.display_menu()
        try:
            user_input = input("Pilihan Anda: ")
            vm.transition(user_input)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    run()
import tkinter as tk
from tkinter import ttk
import math

class SolarCalc:
    def __init__(self, root):
        self.root = root
        self.root.title("Solar Calculator by VH")
        self.root.geometry("540x900")
        self.root.configure(bg="#121212")

        self.quem_manda = "kwh_mes"

        self.vars = {
            "kwh_mes": tk.StringVar(), 
            "kwh_dia": tk.StringVar(value="0.00"),
            "eficiencia": tk.StringVar(value="74"), 
            "radiacao": tk.StringVar(value="5.6"),
            "kwp": tk.StringVar(), 
            "placas": tk.StringVar(), 
            "pot_placa": tk.StringVar(value="700"),
            "equip": tk.StringVar(), 
            "inst_unit": tk.StringVar(value="100"),
            "infra_pct": tk.StringVar(value="7"), 
            "proj": tk.StringVar(value="575"),
            "markup_pct": tk.StringVar(value="25"), 
            "reserva_pct": tk.StringVar(value="5"),
            "imposto_pct": tk.StringVar(value="6")
        }

        self.rs_labels = {}

        for v in self.vars.values():
            v.trace_add("write", self.calcular)

        self.create_widgets()

    def set_mando(self, campo):
        self.quem_manda = campo
        self.calcular()

    def create_widgets(self):
        container = tk.Frame(self.root, bg="#121212", padx=25, pady=20)
        container.pack(fill="both", expand=True)

        def add_row(label, var, name, unit="", readonly=False, show_rs=False):
            frame_main = tk.Frame(container, bg="#121212", pady=4)
            frame_main.pack(fill="x")
            
            row = tk.Frame(frame_main, bg="#121212")
            row.pack(fill="x")
            
            tk.Label(row, text=f"{label} {unit}", bg="#121212", fg="#bbbbbb", font=("Segoe UI", 9)).pack(side="left")
            
            bg_color = "#1e1e1e"
            fg_color = "#f1c40f"
            st = "readonly" if readonly else "normal"
            
            entry = tk.Entry(row, textvariable=var, bg=bg_color, fg=fg_color, 
                             insertbackground="white", borderwidth=0, relief="flat", 
                             justify="right", font=("Segoe UI", 10, "bold"), width=15, 
                             state=st, readonlybackground=bg_color, disabledforeground=fg_color)
            
            if not readonly:
                entry.bind("<FocusIn>", lambda e, n=name: self.set_mando(n))
                entry.bind("<Key>", lambda e, n=name: self.set_mando(n))
            
            entry.pack(side="right", padx=2)

            if show_rs:
                lbl_rs = tk.Label(frame_main, text="= R$ 0,00", bg="#121212", fg="#666666", font=("Segoe UI", 8), anchor="e")
                lbl_rs.pack(fill="x", padx=2)
                self.rs_labels[name] = lbl_rs

            return entry

        tk.Label(container, text="Solar Calculator by VH", bg="#121212", fg="#f1c40f", font=("Segoe UI", 14, "bold")).pack(pady=10)

        self.section_label(container, "DIMENSIONAMENTO")
        add_row("Consumo Mensal", self.vars["kwh_mes"], "kwh_mes", "(kWh/mês)")
        add_row("Consumo Diário", self.vars["kwh_dia"], "kwh_dia", "(kWh/dia)", True)
        add_row("Eficiência", self.vars["eficiencia"], "eficiencia", "(%)")
        add_row("Radiação", self.vars["radiacao"], "radiacao", "(kWh/m²)")
        add_row("Potência de Pico", self.vars["kwp"], "kwp", "(kWp)")
        add_row("Potência Módulo", self.vars["pot_placa"], "pot_placa", "(W)")
        add_row("Nº de Placas", self.vars["placas"], "placas", "(un)")

        self.section_label(container, "CUSTOS DIRETOS")
        add_row("Equipamentos", self.vars["equip"], "equip", "(R$)")
        add_row("Instalação p/ Placa", self.vars["inst_unit"], "inst_unit", "(R$)")
        add_row("Projeto Técnico", self.vars["proj"], "proj", "(R$)")

        self.section_label(container, "TAXAS EM CASCATA")
        add_row("Infraestrutura", self.vars["infra_pct"], "infra_pct", "(%)", show_rs=True)
        add_row("Markup", self.vars["markup_pct"], "markup_pct", "(%)", show_rs=True)
        add_row("Reserva de Caixa", self.vars["reserva_pct"], "reserva_pct", "(%)", show_rs=True)
        add_row("Imposto", self.vars["imposto_pct"], "imposto_pct", "(%)", show_rs=True)

        tk.Frame(container, bg="#f1c40f", height=2).pack(fill="x", pady=20)
        self.lbl_total = tk.Label(container, text="TOTAL: R$ 0,00", bg="#121212", fg="#2ecc71", font=("Segoe UI", 20, "bold"))
        self.lbl_total.pack()
        
        self.lbl_detalhes = tk.Label(container, text="Acompanhamento em R$ ativado", bg="#121212", fg="#555555", font=("Segoe UI", 9), pady=5)
        self.lbl_detalhes.pack()

    def section_label(self, parent, text):
        tk.Label(parent, text=text, bg="#121212", fg="#444444", font=("Segoe UI", 8, "bold"), pady=8).pack(anchor="w")

    def calcular(self, *args):
        try:
            def get_f(name):
                val = self.vars[name].get().replace(",", ".")
                return float(val) if val and val != "." else 0.0

            def fmt(val):
                return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            eff, rad, pot_m = get_f("eficiencia")/100, get_f("radiacao"), get_f("pot_placa")

            if self.quem_manda == "kwh_mes":
                kwh_m = get_f("kwh_mes")
                kwh_d = kwh_m / 30
                self.vars["kwh_dia"].set(f"{kwh_d:.2f}")
                if rad > 0 and eff > 0:
                    self.vars["kwp"].set(f"{(kwh_d / (rad * eff)):.2f}")
            elif self.quem_manda == "kwp":
                kwp_in = get_f("kwp")
                if rad > 0 and eff > 0:
                    kwh_m_calc = kwp_in * rad * eff * 30
                    self.vars["kwh_mes"].set(f"{kwh_m_calc:.2f}")
                    self.vars["kwh_dia"].set(f"{(kwh_m_calc/30):.2f}")

            n_placas = math.ceil((get_f("kwp") * 1000) / pot_m) if pot_m > 0 else 0
            self.vars["placas"].set(str(n_placas))

            base = get_f("equip") + (n_placas * get_f("inst_unit")) + get_f("proj")
            
            valor_infra = base * (get_f("infra_pct") / 100)
            self.rs_labels["infra_pct"].config(text=f"= {fmt(valor_infra)}")
            base += valor_infra
            
            valor_markup = base * (get_f("markup_pct") / 100)
            self.rs_labels["markup_pct"].config(text=f"= {fmt(valor_markup)}")
            base += valor_markup
            
            valor_reserva = base * (get_f("reserva_pct") / 100)
            self.rs_labels["reserva_pct"].config(text=f"= {fmt(valor_reserva)}")
            base += valor_reserva
            
            valor_imposto = base * (get_f("imposto_pct") / 100)
            self.rs_labels["imposto_pct"].config(text=f"= {fmt(valor_imposto)}")
            total_final = base + valor_imposto
            
            self.lbl_total.config(text=f"TOTAL: {fmt(total_final)}")
            
        except Exception:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    app = SolarCalc(root)
    root.mainloop()
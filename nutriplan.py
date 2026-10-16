```html
<!DOCTYPE html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NutriPlán | Kalkulačka kalórií a denník stravy</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts: Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    },
                    colors: {
                        brand: {
                            50: '#ecfdf5',
                            100: '#d1fae5',
                            500: '#10b981',
                            600: '#059669',
                            700: '#047857',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
        }
        /* Plynulé prechody pre SVG kruh */
        .progress-ring__circle {
            transition: stroke-dashoffset 0.5s cubic-bezier(0.4, 0, 0.2, 1), stroke 0.3s ease;
            transform: rotate(-90deg);
            transform-origin: 50% 50%;
        }
        /* Vlastný scrollbar pre zoznamy */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 8px;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 8px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #059669;
            cursor: pointer;
            border: 2px solid white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body class="text-slate-800 antialiased min-h-screen flex flex-col">

    <!-- HLAVIČKA -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center gap-2.5">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white shadow-md shadow-emerald-500/20">
                    <i data-lucide="flame" class="w-6 h-6"></i>
                </div>
                <div>
                    <h1 class="text-lg font-extrabold tracking-tight text-slate-900 leading-none">Nutri<span class="text-emerald-600">Plán</span></h1>
                    <p class="text-xs text-slate-500 font-medium mt-0.5">Kalkulačka kalórií & Denník stravy</p>
                </div>
            </div>
            
            <div class="flex items-center gap-2 sm:gap-3">
                <button onclick="loadDemoDay()" class="inline-flex items-center gap-1.5 px-3 py-2 text-xs sm:text-sm font-medium text-emerald-700 bg-emerald-50 hover:bg-emerald-100 rounded-xl transition-colors" title="Načítať ukážkový jedálniček na celý deň">
                    <i data-lucide="sparkles" class="w-4 h-4"></i>
                    <span>Ukážkový deň</span>
                </button>
                <button onclick="confirmResetDiary()" class="inline-flex items-center gap-1.5 px-3 py-2 text-xs sm:text-sm font-medium text-rose-600 bg-rose-50 hover:bg-rose-100 rounded-xl transition-colors" title="Vymazať dnešný denník">
                    <i data-lucide="trash-2" class="w-4 h-4"></i>
                    <span class="hidden sm:inline">Vyčistiť denník</span>
                </button>
            </div>
        </div>
    </header>

    <!-- HLAVNÝ OBSAH -->
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8 items-start">
            
            <!-- ĽAVÝ STĹPEC: OSOBNÝ PROFIL A VÝPOČET (5 stĺpcov na LG) -->
            <div class="lg:col-span-5 space-y-6">
                
                <!-- Karta: Vstupné údaje -->
                <div class="bg-white rounded-2xl shadow-sm border border-slate-200/80 p-5 sm:p-6">
                    <div class="flex items-center justify-between mb-5">
                        <div class="flex items-center gap-2">
                            <i data-lucide="user-check" class="w-5 h-5 text-emerald-600"></i>
                            <h2 class="text-base sm:text-lg font-bold text-slate-900">1. Osobné parametre</h2>
                        </div>
                        <span class="text-xs font-medium px-2.5 py-1 bg-slate-100 text-slate-600 rounded-full">Mifflin-St Jeor</span>
                    </div>

                    <!-- Pohlavie -->
                    <div class="grid grid-cols-2 gap-3 mb-5">
                        <button type="button" id="btn-male" onclick="setGender('male')" class="flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl font-semibold text-sm border-2 transition-all">
                            <i data-lucide="user" class="w-4 h-4"></i>
                            Muž
                        </button>
                        <button type="button" id="btn-female" onclick="setGender('female')" class="flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl font-semibold text-sm border-2 transition-all">
                            <i data-lucide="user" class="w-4 h-4"></i>
                            Žena
                        </button>
                    </div>

                    <!-- Vek, Výška, Váha -->
                    <div class="space-y-4 mb-6">
                        <!-- Vek -->
                        <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-200/60">
                            <div class="flex justify-between items-center mb-1.5">
                                <label for="input-age" class="text-xs font-semibold uppercase tracking-wider text-slate-500">Vek (roky)</label>
                                <div class="flex items-center gap-1">
                                    <input type="number" id="input-age" min="15" max="100" value="30" oninput="syncProfileInput('age', this.value)" class="w-16 text-right font-bold text-slate-900 bg-white border border-slate-300 rounded-lg px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                                    <span class="text-xs text-slate-500 font-medium">r.</span>
                                </div>
                            </div>
                            <input type="range" id="range-age" min="15" max="100" value="30" oninput="syncProfileInput('age', this.value)" class="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer">
                        </div>

                        <!-- Výška -->
                        <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-200/60">
                            <div class="flex justify-between items-center mb-1.5">
                                <label for="input-height" class="text-xs font-semibold uppercase tracking-wider text-slate-500">Výška (cm)</label>
                                <div class="flex items-center gap-1">
                                    <input type="number" id="input-height" min="130" max="230" value="178" oninput="syncProfileInput('height', this.value)" class="w-16 text-right font-bold text-slate-900 bg-white border border-slate-300 rounded-lg px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                                    <span class="text-xs text-slate-500 font-medium">cm</span>
                                </div>
                            </div>
                            <input type="range" id="range-height" min="130" max="230" value="178" oninput="syncProfileInput('height', this.value)" class="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer">
                        </div>

                        <!-- Váha -->
                        <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-200/60">
                            <div class="flex justify-between items-center mb-1.5">
                                <label for="input-weight" class="text-xs font-semibold uppercase tracking-wider text-slate-500">Hmotnosť (kg)</label>
                                <div class="flex items-center gap-1">
                                    <input type="number" id="input-weight" min="35" max="220" step="0.5" value="78" oninput="syncProfileInput('weight', this.value)" class="w-20 text-right font-bold text-slate-900 bg-white border border-slate-300 rounded-lg px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                                    <span class="text-xs text-slate-500 font-medium">kg</span>
                                </div>
                            </div>
                            <input type="range" id="range-weight" min="35" max="180" step="0.5" value="78" oninput="syncProfileInput('weight', this.value)" class="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer">
                        </div>
                    </div>

                    <!-- Úroveň aktivity -->
                    <div class="mb-6">
                        <label for="select-activity" class="block text-xs font-semibold uppercase tracking-wider text-slate-500 mb-2">Úroveň pohybovej aktivity</label>
                        <div class="relative">
                            <select id="select-activity" onchange="updateProfile()" class="w-full bg-slate-50 border border-slate-300 text-slate-900 text-sm rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 block p-3 pr-8 font-medium appearance-none cursor-pointer">
                                <option value="1.2">Sedavý spôsob (minimum pohybu, práca v kancelárii)</option>
                                <option value="1.375" selected>Mierne aktívny (ľahké cvičenie / šport 1–3x týždenne)</option>
                                <option value="1.55">Stredne aktívny (intenzívnejší šport 3–5x týždenne)</option>
                                <option value="1.725">Veľmi aktívny (náročný tréning 6–7x týždenne)</option>
                                <option value="1.9">Extrémne aktívny (manuálna práca + denný tréning)</option>
                            </select>
                            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-slate-500">
                                <i data-lucide="chevron-down" class="w-4 h-4"></i>
                            </div>
                        </div>
                    </div>

                    <!-- Cieľ -->
                    <div class="mb-6">
                        <label class="block text-xs font-semibold uppercase tracking-wider text-slate-500 mb-2">Váš hlavný cieľ</label>
                        <div class="grid grid-cols-3 gap-2.5">
                            <button type="button" id="goal-lose" onclick="setGoal('lose')" class="flex flex-col items-center justify-center p-3 rounded-xl border-2 text-center transition-all">
                                <i data-lucide="trending-down" class="w-5 h-5 mb-1"></i>
                                <span class="text-xs font-bold">Chudnutie</span>
                                <span class="text-[10px] opacity-75 mt-0.5">-20% kcal</span>
                            </button>
                            <button type="button" id="goal-maintain" onclick="setGoal('maintain')" class="flex flex-col items-center justify-center p-3 rounded-xl border-2 text-center transition-all">
                                <i data-lucide="scale" class="w-5 h-5 mb-1"></i>
                                <span class="text-xs font-bold">Udržiavanie</span>
                                <span class="text-[10px] opacity-75 mt-0.5">TDEE rovnováha</span>
                            </button>
                            <button type="button" id="goal-gain" onclick="setGoal('gain')" class="flex flex-col items-center justify-center p-3 rounded-xl border-2 text-center transition-all">
                                <i data-lucide="trending-up" class="w-5 h-5 mb-1"></i>
                                <span class="text-xs font-bold">Naberanie</span>
                                <span class="text-[10px] opacity-75 mt-0.5">+15% kcal</span>
                            </button>
                        </div>
                    </div>

                    <!-- Štýl rozloženia makroživín -->
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <label for="select-macro-split" class="block text-xs font-semibold uppercase tracking-wider text-slate-500">Pomer makroživín (B / S / T)</label>
                            <span id="macro-ratio-badge" class="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md">30% / 40% / 30%</span>
                        </div>
                        <div class="relative">
                            <select id="select-macro-split" onchange="updateProfile()" class="w-full bg-slate-50 border border-slate-300 text-slate-900 text-sm rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 block p-2.5 pr-8 font-medium appearance-none cursor-pointer">
                                <option value="recommended" selected>Odporúčaný podľa cieľa (Optimálny)</option>
                                <option value="balanced">Vyvážený štandard (25% B / 50% S / 25% T)</option>
                                <option value="highprotein">Vysokobielkovinový fitness (35% B / 40% S / 25% T)</option>
                                <option value="lowcarb">Nízkosacharidový / Low-Carb (35% B / 20% S / 45% T)</option>
                            </select>
                            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-slate-500">
                                <i data-lucide="sliders" class="w-4 h-4"></i>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Karta: Výsledky metabolizmu (BMR, TDEE, BMI, Ciele) -->
                <div class="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white rounded-2xl shadow-lg p-5 sm:p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-base font-bold flex items-center gap-2">
                            <i data-lucide="activity" class="w-5 h-5 text-emerald-400"></i>
                            Analýza metabolizmu a denný cieľ
                        </h3>
                        <span id="bmi-badge" class="text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                            BMI: 24.6 (Norma)
                        </span>
                    </div>

                    <!-- BMR, TDEE, Cieľ box -->
                    <div class="grid grid-cols-3 gap-3 mb-5">
                        <div class="bg-white/5 border border-white/10 rounded-xl p-3 text-center">
                            <div class="text-[11px] text-slate-400 uppercase font-semibold tracking-wider">BMR (Pokojový)</div>
                            <div class="text-lg sm:text-xl font-extrabold text-white mt-1"><span id="res-bmr">1760</span></div>
                            <div class="text-[10px] text-slate-400">kcal / deň</div>
                        </div>
                        <div class="bg-white/5 border border-white/10 rounded-xl p-3 text-center">
                            <div class="text-[11px] text-slate-400 uppercase font-semibold tracking-wider">TDEE (Výdaj)</div>
                            <div class="text-lg sm:text-xl font-extrabold text-white mt-1"><span id="res-tdee">2420</span></div>
                            <div class="text-[10px] text-slate-400">kcal / deň</div>
                        </div>
                        <div class="bg-emerald-500/20 border border-emerald-500/40 rounded-xl p-3 text-center">
                            <div class="text-[11px] text-emerald-300 uppercase font-bold tracking-wider">Váš Cieľ</div>
                            <div class="text-lg sm:text-xl font-black text-emerald-400 mt-1"><span id="res-target">1936</span></div>
                            <div class="text-[10px] text-emerald-200">kcal / deň</div>
                        </div>
                    </div>

                    <!-- Odporúčané denné makroživiny -->
                    <div class="space-y-2.5 pt-2 border-t border-white/10">
                        <div class="text-xs font-semibold text-slate-300 mb-2">Odporúčané denné makroživiny:</div>
                        <div class="grid grid-cols-3 gap-2.5">
                            <div class="bg-blue-500/10 border border-blue-500/30 rounded-xl p-2.5">
                                <div class="flex items-center justify-between text-xs text-blue-300 font-semibold">
                                    <span>Bielkoviny</span>
                                    <span id="res-p-pct" class="text-[10px] opacity-80">30%</span>
                                </div>
                                <div class="text-base sm:text-lg font-extrabold text-white mt-0.5"><span id="res-p-grams">145</span> g</div>
                                <div class="text-[10px] text-slate-400"><span id="res-p-kcal">580</span> kcal</div>
                            </div>
                            <div class="bg-amber-500/10 border border-amber-500/30 rounded-xl p-2.5">
                                <div class="flex items-center justify-between text-xs text-amber-300 font-semibold">
                                    <span>Sacharidy</span>
                                    <span id="res-c-pct" class="text-[10px] opacity-80">40%</span>
                                </div>
                                <div class="text-base sm:text-lg font-extrabold text-white mt-0.5"><span id="res-c-grams">194</span> g</div>
                                <div class="text-[10px] text-slate-400"><span id="res-c-kcal">776</span> kcal</div>
                            </div>
                            <div class="bg-rose-500/10 border border-rose-500/30 rounded-xl p-2.5">
                                <div class="flex items-center justify-between text-xs text-rose-300 font-semibold">
                                    <span>Tuky</span>
                                    <span id="res-f-pct" class="text-[10px] opacity-80">30%</span>
                                </div>
                                <div class="text-base sm:text-lg font-extrabold text-white mt-0.5"><span id="res-f-grams">65</span> g</div>
                                <div class="text-[10px] text-slate-400"><span id="res-f-kcal">585</span> kcal</div>
                            </div>
                        </div>
                    </div>

                    <!-- Vysvetlivka -->
                    <p class="text-[11px] text-slate-400 mt-4 leading-relaxed">
                        <strong class="text-slate-200">BMR</strong> je energia potrebná na základné životné funkcie v pokoji. <strong class="text-slate-200">TDEE</strong> zahŕňa aj váš denný pohyb. Cieľové kalórie sú automaticky prepojené s vaším denníkom stravy vpravo.
                    </p>
                </div>

                <!-- Karta: Pitný režim -->
                <div class="bg-white rounded-2xl shadow-sm border border-slate-200/80 p-5">
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-2">
                            <div class="w-8 h-8 rounded-lg bg-sky-100 text-sky-600 flex items-center justify-center">
                                <i data-lucide="droplets" class="w-5 h-5"></i>
                            </div>
                            <div>
                                <h3 class="text-sm font-bold text-slate-900">Pitný režim</h3>
                                <p class="text-xs text-slate-500">Odporúčanie podľa váhy: <strong id="water-target-text" class="text-slate-700">2.7 l</strong></p>
                            </div>
                        </div>
                        <div class="text-right">
                            <span id="water-current-text" class="text-lg font-extrabold text-sky-600">0.0</span>
                            <span class="text-xs font-semibold text-slate-400">/ <span id="water-goal-num">2.7</span> l</span>
                        </div>
                    </div>

                    <div class="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden mb-3">
                        <div id="water-progress-bar" class="bg-gradient-to-r from-sky-400 to-blue-600 h-full rounded-full transition-all duration-300" style="width: 0%"></div>
                    </div>

                    <div class="flex items-center justify-between gap-2">
                        <div class="flex gap-1.5">
                            <button onclick="addWater(250)" class="px-3 py-1.5 bg-sky-50 hover:bg-sky-100 text-sky-700 rounded-lg text-xs font-semibold transition-colors flex items-center gap-1">
                                <i data-lucide="plus" class="w-3.5 h-3.5"></i> 250 ml (Pohár)
                            </button>
                            <button onclick="addWater(500)" class="px-3 py-1.5 bg-sky-50 hover:bg-sky-100 text-sky-700 rounded-lg text-xs font-semibold transition-colors flex items-center gap-1">
                                <i data-lucide="plus" class="w-3.5 h-3.5"></i> 500 ml (Fľaša)
                            </button>
                        </div>
                        <button onclick="resetWater()" class="text-xs text-slate-400 hover:text-slate-600 px-2 py-1">Vynulovať</button>
                    </div>
                </div>

            </div>

            <!-- PRAVÝ STĹPEC: PREHĽAD DŇA A INTERAKTÍVNY DENNÍK STRAVY (7 stĺpcov na LG) -->
            <div class="lg:col-span-7 space-y-6">

                <!-- Karta: Dnešný progres (Grafy a ukazovatele) -->
                <div class="bg-white rounded-2xl shadow-sm border border-slate-200/80 p-5 sm:p-6">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-5">
                        <div class="flex items-center gap-2">
                            <i data-lucide="pie-chart" class="w-5 h-5 text-emerald-600"></i>
                            <h2 class="text-base sm:text-lg font-bold text-slate-900">2. Dnešný prehľad a plnenie cieľa</h2>
                        </div>
                        <span id="status-pill" class="text-xs font-semibold px-3 py-1 rounded-full bg-emerald-50 text-emerald-700">
                            V norme
                        </span>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
                        <!-- Kruhový graf kalórií -->
                        <div class="md:col-span-5 flex flex-col items-center justify-center">
                            <div class="relative w-44 h-44 flex items-center justify-center">
                                <svg class="w-full h-full" viewBox="0 0 160 160">
                                    <!-- Pozadie kruhu -->
                                    <circle cx="80" cy="80" r="66" stroke="#f1f5f9" stroke-width="14" fill="transparent" />
                                    <!-- Progres kruh -->
                                    <circle id="calorie-ring" class="progress-ring__circle" cx="80" cy="80" r="66" stroke="#10b981" stroke-width="14" stroke-linecap="round" fill="transparent" stroke-dasharray="414.69" stroke-dashoffset="414.69" />
                                </svg>
                                <div class="absolute inset-0 flex flex-col items-center justify-center text-center px-4">
                                    <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400" id="ring-label">Zostáva</span>
                                    <span class="text-3xl font-black text-slate-900 tracking-tight my-0.5" id="ring-main-value">1936</span>
                                    <span class="text-xs font-medium text-slate-500">z <span id="ring-target-value">1936</span> kcal</span>
                                </div>
                            </div>

                            <div class="grid grid-cols-2 gap-4 w-full mt-3 pt-3 border-t border-slate-100 text-center">
                                <div>
                                    <div class="text-[11px] text-slate-400 font-semibold uppercase">Prijaté dnes</div>
                                    <div class="text-base font-extrabold text-slate-800"><span id="eaten-kcal">0</span> kcal</div>
                                </div>
                                <div>
                                    <div class="text-[11px] text-slate-400 font-semibold uppercase">Splnené</div>
                                    <div class="text-base font-extrabold text-emerald-600"><span id="eaten-pct">0</span> %</div>
                                </div>
                            </div>
                        </div>

                        <!-- Ukazovatele makroživín -->
                        <div class="md:col-span-7 space-y-5">
                            <!-- Bielkoviny -->
                            <div>
                                <div class="flex justify-between items-end mb-1.5">
                                    <div class="flex items-center gap-2">
                                        <span class="w-3 h-3 rounded-full bg-blue-500 inline-block"></span>
                                        <span class="text-sm font-bold text-slate-800">Bielkoviny</span>
                                    </div>
                                    <div class="text-xs font-semibold text-slate-600">
                                        <span id="eaten-p" class="text-sm font-extrabold text-slate-900">0</span> / <span id="goal-p">145</span> g
                                        <span id="diff-p" class="ml-1.5 text-[11px] text-slate-400">(zostáva 145 g)</span>
                                    </div>
                                </div>
                                <div class="w-full bg-slate-100 h-3 rounded-full overflow-hidden">
                                    <div id="bar-p" class="bg-blue-500 h-full rounded-full transition-all duration-500" style="width: 0%"></div>
                                </div>
                            </div>

                            <!-- Sacharidy -->
                            <div>
                                <div class="flex justify-between items-end mb-1.5">
                                    <div class="flex items-center gap-2">
                                        <span class="w-3 h-3 rounded-full bg-amber-500 inline-block"></span>
                                        <span class="text-sm font-bold text-slate-800">Sacharidy</span>
                                    </div>
                                    <div class="text-xs font-semibold text-slate-600">
                                        <span id="eaten-c" class="text-sm font-extrabold text-slate-900">0</span> / <span id="goal-c">194</span> g
                                        <span id="diff-c" class="ml-1.5 text-[11px] text-slate-400">(zostáva 194 g)</span>
                                    </div>
                                </div>
                                <div class="w-full bg-slate-100 h-3 rounded-full overflow-hidden">
                                    <div id="bar-c" class="bg-amber-500 h-full rounded-full transition-all duration-500" style="width: 0%"></div>
                                </div>
                            </div>

                            <!-- Tuky -->
                            <div>
                                <div class="flex justify-between items-end mb-1.5">
                                    <div class="flex items-center gap-2">
                                        <span class="w-3 h-3 rounded-full bg-rose-500 inline-block"></span>
                                        <span class="text-sm font-bold text-slate-800">Tuky</span>
                                    </div>
                                    <div class="text-xs font-semibold text-slate-600">
                                        <span id="eaten-f" class="text-sm font-extrabold text-slate-900">0</span> / <span id="goal-f">65</span> g
                                        <span id="diff-f" class="ml-1.5 text-[11px] text-slate-400">(zostáva 65 g)</span>
                                    </div>
                                </div>
                                <div class="w-full bg-slate-100 h-3 rounded-full overflow-hidden">
                                    <div id="bar-f" class="bg-rose-500 h-full rounded-full transition-all duration-500" style="width: 0%"></div>
                                </div>
                            </div>

                            <!-- Pomer prijatých kalórií z makier -->
                            <div class="pt-2">
                                <div class="flex justify-between text-[11px] text-slate-500 font-medium mb-1">
                                    <span>Skutočný pomer prijatých kalórií (B / S / T)</span>
                                    <span id="actual-macro-split-text">0% / 0% / 0%</span>
                                </div>
                                <div class="w-full h-2 bg-slate-100 rounded-full overflow-hidden flex">
                                    <div id="split-bar-p" class="bg-blue-500 h-full transition-all duration-300" style="width: 0%"></div>
                                    <div id="split-bar-c" class="bg-amber-500 h-full transition-all duration-300" style="width: 0%"></div>
                                    <div id="split-bar-f" class="bg-rose-500 h-full transition-all duration-300" style="width: 0%"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Karta: Pridanie jedla do denníka -->
                <div class="bg-white rounded-2xl shadow-sm border border-slate-200/80 p-5 sm:p-6">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-5">
                        <div class="flex items-center gap-2">
                            <i data-lucide="utensils" class="w-5 h-5 text-emerald-600"></i>
                            <h2 class="text-base sm:text-lg font-bold text-slate-900">3. Pridať jedlo do denníka</h2>
                        </div>

                        <!-- Prepínač režimu: Databáza vs Vlastné jedlo -->
                        <div class="inline-flex bg-slate-100 p-1 rounded-xl self-start sm:self-auto">
                            <button type="button" id="tab-db" onclick="switchFoodTab('db')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition-all bg-white text-slate-900 shadow-sm">
                                Zoznam potravín
                            </button>
                            <button type="button" id="tab-custom" onclick="switchFoodTab('custom')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition-all text-slate-600 hover:text-slate-900">
                                Vlastné hodnoty
                            </button>
                        </div>
                    </div>

                    <!-- Výber chodu dňa (Raňajky, Obed, Večera, Snack) -->
                    <div class="mb-4">
                        <label class="block text-xs font-semibold uppercase tracking-wider text-slate-500 mb-2">Kategória jedla (Chod)</label>
                        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                            <button type="button" onclick="selectMealCategory('ranajky')" id="cat-ranajky" class="meal-cat-btn flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl text-xs font-bold border transition-all">
                                <span>🌅</span> Raňajky
                            </button>
                            <button type="button" onclick="selectMealCategory('obed')" id="cat-obed" class="meal-cat-btn flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl text-xs font-bold border transition-all">
                                <span>☀️</span> Obed
                            </button>
                            <button type="button" onclick="selectMealCategory('vecera')" id="cat-vecera" class="meal-cat-btn flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl text-xs font-bold border transition-all">
                                <span>🌙</span> Večera
                            </button>
                            <button type="button" onclick="selectMealCategory('snack')" id="cat-snack" class="meal-cat-btn flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl text-xs font-bold border transition-all">
                                <span>🍎</span> Snack / Iné
                            </button>
                        </div>
                    </div>

                    <!-- PANEL A: Výber z preddefinovanej databázy potravín -->
                    <div id="panel-db" class="space-y-4">
                        <div class="grid grid-cols-1 sm:grid-cols-12 gap-3">
                            <!-- Vyhľadávanie a filter -->
                            <div class="sm:col-span-5 relative">
                                <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
                                <input type="text" id="food-search" oninput="filterFoodDatabase()" placeholder="Hľadať (napr. kuracie, tvaroh, ryža...)" class="w-full pl-9 pr-3 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                            </div>

                            <!-- Výber potraviny -->
                            <div class="sm:col-span-7 relative">
                                <select id="food-select" onchange="onFoodSelectChange()" class="w-full py-2.5 px-3 pr-8 bg-slate-50 border border-slate-300 rounded-xl text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 appearance-none cursor-pointer">
                                    <!-- Naplnené cez JS -->
                                </select>
                                <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-slate-500">
                                    <i data-lucide="chevron-down" class="w-4 h-4"></i>
                                </div>
                            </div>
                        </div>

                        <!-- Množstvo (gramáž) a rýchle porcie -->
                        <div class="bg-slate-50 p-4 rounded-xl border border-slate-200/70">
                            <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
                                <div class="flex items-center gap-2">
                                    <label for="food-grams" class="text-xs font-bold uppercase text-slate-600">Množstvo (g / ml):</label>
                                    <input type="number" id="food-grams" value="100" min="1" max="2000" oninput="updateDbFoodPreview()" class="w-24 font-extrabold text-center text-slate-900 bg-white border border-slate-300 rounded-lg py-1.5 px-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                                    <span class="text-xs text-slate-500 font-medium">g</span>
                                </div>

                                <!-- Rýchle tlačidlá gramáže -->
                                <div class="flex flex-wrap items-center gap-1.5">
                                    <button type="button" id="btn-portion-default" onclick="setQuickGrams('portion')" class="px-2.5 py-1 bg-emerald-100 hover:bg-emerald-200 text-emerald-800 rounded-lg text-xs font-semibold transition-colors">
                                        Bežná porcia (150g)
                                    </button>
                                    <button type="button" onclick="setQuickGrams(50)" class="px-2 py-1 bg-white border border-slate-200 hover:bg-slate-100 text-slate-700 rounded-lg text-xs font-medium transition-colors">50g</button>
                                    <button type="button" onclick="setQuickGrams(100)" class="px-2 py-1 bg-white border border-slate-200 hover:bg-slate-100 text-slate-700 rounded-lg text-xs font-medium transition-colors">100g</button>
                                    <button type="button" onclick="setQuickGrams(150)" class="px-2 py-1 bg-white border border-slate-200 hover:bg-slate-100 text-slate-700 rounded-lg text-xs font-medium transition-colors">150g</button>
                                    <button type="button" onclick="setQuickGrams(250)" class="px-2 py-1 bg-white border border-slate-200 hover:bg-slate-100 text-slate-700 rounded-lg text-xs font-medium transition-colors">250g</button>
                                </div>
                            </div>

                            <!-- Náhľad hodnôt pred pridaním -->
                            <div class="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-200/80">
                                <div class="flex flex-wrap items-center gap-3 text-xs">
                                    <span class="font-bold text-slate-900 bg-white px-2.5 py-1 rounded-lg border border-slate-200 shadow-2xs">
                                        🔥 <span id="preview-kcal">0</span> kcal
                                    </span>
                                    <span class="font-semibold text-blue-700 bg-blue-50 px-2.5 py-1 rounded-lg">
                                        B: <span id="preview-p">0</span> g
                                    </span>
                                    <span class="font-semibold text-amber-700 bg-amber-50 px-2.5 py-1 rounded-lg">
                                        S: <span id="preview-c">0</span> g
                                    </span>
                                    <span class="font-semibold text-rose-700 bg-rose-50 px-2.5 py-1 rounded-lg">
                                        T: <span id="preview-f">0</span> g
                                    </span>
                                </div>

                                <button type="button" onclick="addSelectedDbFood()" class="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm rounded-xl shadow-sm shadow-emerald-600/20 transition-all cursor-pointer">
                                    <i data-lucide="plus-circle" class="w-4 h-4"></i>
                                    Pridať do denníka
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- PANEL B: Vlastné jedlo (Manuálne zadanie) -->
                    <div id="panel-custom" class="hidden space-y-4">
                        <div class="bg-slate-50 p-4 rounded-xl border border-slate-200/70 space-y-4">
                            <div class="grid grid-cols-1 sm:grid-cols-12 gap-3">
                                <div class="sm:col-span-8">
                                    <label class="block text-xs font-semibold text-slate-600 mb-1">Názov jedla / potraviny *</label>
                                    <input type="text" id="custom-name" placeholder="Napr. Domáci протеínový koláč, Obedové menu..." class="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                                </div>
                                <div class="sm:col-span-4">
                                    <label class="block text-xs font-semibold text-slate-600 mb-1">Hmotnosť porcie (g)</label>
                                    <input type="number" id="custom-grams" value="100" min="1" class="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                                </div>
                            </div>

                            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                                <div>
                                    <label class="block text-xs font-semibold text-blue-600 mb-1">Bielkoviny (g)</label>
                                    <input type="number" id="custom-p" value="15" min="0" step="0.5" oninput="autoCalcCustomKcal()" class="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-blue-500">
                                </div>
                                <div>
                                    <label class="block text-xs font-semibold text-amber-600 mb-1">Sacharidy (g)</label>
                                    <input type="number" id="custom-c" value="30" min="0" step="0.5" oninput="autoCalcCustomKcal()" class="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-amber-500">
                                </div>
                                <div>
                                    <label class="block text-xs font-semibold text-rose-600 mb-1">Tuky (g)</label>
                                    <input type="number" id="custom-f" value="10" min="0" step="0.5" oninput="autoCalcCustomKcal()" class="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-rose-500">
                                </div>
                                <div>
                                    <label class="block text-xs font-semibold text-slate-700 mb-1">Kalórie (kcal) *</label>
                                    <input type="number" id="custom-kcal" value="270" min="0" class="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-extrabold text-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500">
                                </div>
                            </div>

                            <div class="flex flex-wrap items-center justify-between gap-2 pt-2">
                                <span class="text-[11px] text-slate-500">Tip: Kalórie sa automaticky prepočítavajú podľa vzorca (4×B + 4×S + 9×T), ale môžete ich aj upraviť.</span>
                                <button type="button" onclick="addCustomFood()" class="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm rounded-xl shadow-sm transition-all cursor-pointer">
                                    <i data-lucide="plus-circle" class="w-4 h-4"></i>
                                    Pridať vlastné jedlo
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Karta: Zoznam prijatých jedál podľa chodov -->
                <div class="bg-white rounded-2xl shadow-sm border border-slate-200/80 p-5 sm:p-6">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center gap-2">
                            <i data-lucide="book-open" class="w-5 h-5 text-emerald-600"></i>
                            <h2 class="text-base sm:text-lg font-bold text-slate-900">4. Dnešný záznam jedál</h2>
                        </div>
                        <span id="diary-count-badge" class="text-xs font-semibold text-slate-500 bg-slate-100 px-2.5 py-1 rounded-full">0 položiek</span>
                    </div>

                    <div id="diary-sections-container" class="space-y-4">
                        <!-- Dynamicky generované sekcie: Raňajky, Obed, Večera, Snack -->
                    </div>
                </div>

            </div>
        </div>
    </main>

    <!-- NOTIFIKAČNÝ TOAST -->
    <div id="toast-container" class="fixed bottom-5 right-5 z-50 pointer-events-none flex flex-col gap-2"></div>

    <!-- MODÁLNE OKNO PRE POTVRDENIE VYMAZANIA (Namiesto alert/confirm) -->
    <div id="confirm-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4">
        <div class="bg-white rounded-2xl max-w-sm w-full p-6 shadow-xl border border-slate-200 animate-fade-in">
            <div class="w-12 h-12 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center mb-4">
                <i data-lucide="alert-triangle" class="w-6 h-6"></i>
            </div>
            <h3 class="text-lg font-bold text-slate-900 mb-1">Vyčistiť dnešný denník?</h3>
            <p class="text-sm text-slate-600 mb-6">Naozaj chcete odstrániť všetky dnes zaznamenané jedlá? Vaše osobné nastavenia a výpočty zostanú zachované.</p>
            <div class="flex items-center justify-end gap-3">
                <button onclick="closeConfirmModal()" class="px-4 py-2 rounded-xl text-sm font-semibold text-slate-600 hover:bg-slate-100 transition-colors">Zrušiť</button>
                <button onclick="executeResetDiary()" class="px-4 py-2 rounded-xl text-sm font-semibold bg-rose-600 hover:bg-rose-700 text-white transition-colors">Áno, vymazať</button>
            </div>
        </div>
    </div>

    <!-- JAVASCRIPT LOGIKA -->
    <script>
        // ==========================================
        // 1. DATABÁZA BEŽNÝCH POTRAVÍN (Hodnoty na 100g)
        // ==========================================
        const FOOD_DATABASE = [
            // Mäso, ryby a vajíčka
            { id: 'kuracie_prsia', name: 'Kuracie prsia (surové)', group: 'Mäso, ryby a vajcia', kcal: 110, p: 23.1, c: 0, f: 1.2, portion: 150, portionName: '150g porcia' },
            { id: 'morcacie_prsia', name: 'Morčacie prsia', group: 'Mäso, ryby a vajcia', kcal: 107, p: 24.0, c: 0, f: 1.0, portion: 150, portionName: '150g porcia' },
            { id: 'hovadzie_zadne', name: 'Hovädzie mäso chudé (zadné)', group: 'Mäso, ryby a vajcia', kcal: 158, p: 21.5, c: 0, f: 7.5, portion: 150, portionName: '150g porcia' },
            { id: 'bravcove_karé', name: 'Bravčové karé (chudé)', group: 'Mäso, ryby a vajcia', kcal: 143, p: 21.0, c: 0, f: 6.3, portion: 150, portionName: '150g porcia' },
            { id: 'losos', name: 'Losos (filet)', group: 'Mäso, ryby a vajcia', kcal: 208, p: 20.4, c: 0, f: 13.4, portion: 150, portionName: '150g filet' },
            { id: 'tuniak_vlastna', name: 'Tuniak vo vlastnej šťave', group: 'Mäso, ryby a vajcia', kcal: 103, p: 23.5, c: 0, f: 0.8, portion: 130, portionName: '1 konzerva (130g)' },
            { id: 'vajce_cele', name: 'Slepačie vajce (celé, varené)', group: 'Mäso, ryby a vajcia', kcal: 155, p: 12.6, c: 1.1, f: 10.6, portion: 110, portionName: '2 ks vajec (110g)' },
            { id: 'sunka_kuracia', name: 'Kuracia šunka (90% mäsa)', group: 'Mäso, ryby a vajcia', kcal: 98, p: 19.0, c: 1.0, f: 2.0, portion: 50, portionName: '3-4 plátky (50g)' },

            // Mliečne výrobky a alternatívy
            { id: 'tvaroh_jemny', name: 'Tvaroh odtučnený / jemný', group: 'Mliečne výrobky', kcal: 68, p: 12.5, c: 3.8, f: 0.4, portion: 125, portionName: '1/2 balenia (125g)' },
            { id: 'tvaroh_hrudkovity', name: 'Tvaroh hrudkovitý polotučný', group: 'Mliečne výrobky', kcal: 105, p: 18.0, c: 3.5, f: 2.2, portion: 125, portionName: '1/2 balenia (125g)' },
            { id: 'grecky_jogurt', name: 'Grécky jogurt biely (0% tuku)', group: 'Mliečne výrobky', kcal: 57, p: 10.3, c: 4.0, f: 0.2, portion: 140, portionName: '1 téglik (140g)' },
            { id: 'jogurt_biely', name: 'Jogurt biely klasický (3.5% tuku)', group: 'Mliečne výrobky', kcal: 65, p: 4.1, c: 4.5, f: 3.5, portion: 150, portionName: '1 téglik (150g)' },
            { id: 'cottage_cheese', name: 'Cottage Cheese biely', group: 'Mliečne výrobky', kcal: 101, p: 12.5, c: 3.0, f: 4.2, portion: 150, portionName: '1 balenie (150g)' },
            { id: 'skyr_biely', name: 'Skyr biely natur', group: 'Mliečne výrobky', kcal: 63, p: 11.0, c: 4.0, f: 0.2, portion: 140, portionName: '1 téglik (140g)' },
            { id: 'syr_eidam30', name: 'Syr Eidam 30%', group: 'Mliečne výrobky', kcal: 263, p: 27.0, c: 1.5, f: 16.0, portion: 40, portionName: '2 plátky (40g)' },
            { id: 'mozzarella_light', name: 'Mozzarella Light', group: 'Mliečne výrobky', kcal: 165, p: 19.5, c: 1.5, f: 9.0, portion: 125, portionName: '1 balenie (125g)' },
            { id: 'bryndza', name: 'Slovenská bryndza (plnotučná)', group: 'Mliečne výrobky', kcal: 268, p: 14.5, c: 2.0, f: 22.5, portion: 60, portionName: '1 porcia (60g)' },
            { id: 'mlieko_polo', name: 'Mlieko polotučné (1,5%)', group: 'Mliečne výrobky', kcal: 47, p: 3.4, c: 4.8, f: 1.5, portion: 250, portionName: '1 pohár (250ml)' },
            { id: 'whey_protein', name: 'Srvátkový proteín (Whey 80%)', group: 'Mliečne výrobky', kcal: 385, p: 78.0, c: 6.5, f: 5.5, portion: 30, portionName: '1 odmerka (30g)' },

            // Prílohy, obilniny a pečivo
            { id: 'ovsene_vlocky', name: 'Ovsené vločky', group: 'Prílohy a pečivo', kcal: 375, p: 13.5, c: 60.0, f: 7.0, portion: 60, portionName: '1 miska (60g)' },
            { id: 'ryza_varena', name: 'Ryža biela / jazmínová (varená)', group: 'Prílohy a pečivo', kcal: 130, p: 2.7, c: 28.2, f: 0.3, portion: 180, portionName: '1 príloha (180g)' },
            { id: 'ryza_surova', name: 'Ryža (surová pred varením)', group: 'Prílohy a pečivo', kcal: 350, p: 7.5, c: 77.5, f: 0.8, portion: 75, portionName: '1 porcia surová (75g)' },
            { id: 'zemiaky_varene', name: 'Zemiaky varené v šupke', group: 'Prílohy a pečivo', kcal: 77, p: 2.0, c: 17.0, f: 0.1, portion: 220, portionName: '1 príloha (220g)' },
            { id: 'bataty', name: 'Sladké zemiaky (Batáty)', group: 'Prílohy a pečivo', kcal: 86, p: 1.6, c: 20.1, f: 0.1, portion: 200, portionName: '1 príloha (200g)' },
            { id: 'cestoviny_varene', name: 'Cestoviny (varené)', group: 'Prílohy a pečivo', kcal: 158, p: 5.8, c: 30.9, f: 0.9, portion: 180, portionName: '1 porcia (180g)' },
            { id: 'chlieb_kvaskovy', name: 'Chlieb ražný / kváskový', group: 'Prílohy a pečivo', kcal: 235, p: 7.5, c: 46.5, f: 1.4, portion: 80, portionName: '2 krajce (80g)' },
            { id: 'rozok_biely', name: 'Pečivo: Klasický rožok / žemľa', group: 'Prílohy a pečivo', kcal: 295, p: 9.2, c: 57.5, f: 2.8, portion: 50, portionName: '1 kus (50g)' },
            { id: 'tortilla_wrap', name: 'Celozrnná tortilla (Wrap)', group: 'Prílohy a pečivo', kcal: 298, p: 8.5, c: 49.0, f: 6.5, portion: 62, portionName: '1 placka (62g)' },

            // Strukoviny a rastlinné bielkoviny
            { id: 'tofu_natural', name: 'Tofu (Natural / Údené)', group: 'Strukoviny a rastlinné', kcal: 125, p: 15.0, c: 2.0, f: 6.5, portion: 180, portionName: '1 balenie (180g)' },
            { id: 'sosovica_varena', name: 'Šošovica (varená)', group: 'Strukoviny a rastlinné', kcal: 116, p: 9.0, c: 20.1, f: 0.4, portion: 150, portionName: '1 porcia (150g)' },
            { id: 'cicer_steril', name: 'Cícer (varený / sterilizovaný)', group: 'Strukoviny a rastlinné', kcal: 139, p: 7.5, c: 21.0, f: 2.6, portion: 130, portionName: '1 porcia (130g)' },
            { id: 'fazula_cervena', name: 'Červená fazuľa (sterilizovaná)', group: 'Strukoviny a rastlinné', kcal: 108, p: 7.8, c: 16.5, f: 0.6, portion: 120, portionName: '1 porcia (120g)' },

            // Ovocie a zelenina
            { id: 'banan', name: 'Banán', group: 'Ovocie a zelenina', kcal: 89, p: 1.1, c: 22.8, f: 0.3, portion: 120, portionName: '1 stredný kus (120g)' },
            { id: 'jablko', name: 'Jablko', group: 'Ovocie a zelenina', kcal: 52, p: 0.3, c: 13.8, f: 0.2, portion: 150, portionName: '1 stredný kus (150g)' },
            { id: 'cucoriedky', name: 'Čučoriedky / Lesné ovocie', group: 'Ovocie a zelenina', kcal: 57, p: 0.7, c: 14.5, f: 0.3, portion: 100, portionName: '1 hrsť / miska (100g)' },
            { id: 'avokado', name: 'Avokádo', group: 'Ovocie a zelenina', kcal: 160, p: 2.0, c: 8.5, f: 14.7, portion: 70, portionName: '1/2 avokáda (70g)' },
            { id: 'zelenina_mix', name: 'Čerstvá zelenina (paradajka, paprika, uhorka)', group: 'Ovocie a zelenina', kcal: 22, p: 0.9, c: 4.2, f: 0.2, portion: 150, portionName: '1 tanier (150g)' },
            { id: 'brokolica', name: 'Brokolica (parená / surová)', group: 'Ovocie a zelenina', kcal: 34, p: 2.8, c: 6.6, f: 0.4, portion: 150, portionName: '1 porcia (150g)' },

            // Zdravé tuky, orechy a ostatné
            { id: 'arasidove_maslo', name: 'Arašidové maslo (100%)', group: 'Orechy a tuky', kcal: 588, p: 25.8, c: 16.0, f: 50.0, portion: 20, portionName: '1 ČL vrchovatá (20g)' },
            { id: 'mandle_orechy', name: 'Mandle / Vlašské orechy', group: 'Orechy a tuky', kcal: 590, p: 21.0, c: 19.0, f: 52.0, portion: 30, portionName: '1 hrsť (30g)' },
            { id: 'olivovy_olej', name: 'Olivový olej (Extra Virgin)', group: 'Orechy a tuky', kcal: 884, p: 0, c: 0, f: 100.0, portion: 10, portionName: '1 polievková lyžica (10ml)' },
            { id: 'maslo_82', name: 'Maslo klasické (82%)', group: 'Orechy a tuky', kcal: 748, p: 0.7, c: 0.6, f: 82.5, portion: 15, portionName: '1 porcia (15g)' },
            { id: 'horka_cokolada', name: 'Horká čokoláda (70-85%)', group: 'Orechy a tuky', kcal: 580, p: 8.5, c: 34.0, f: 43.0, portion: 25, portionName: '2-3 kocky (25g)' },

            // Hotové jedlá (Slovenské klasiky)
            { id: 'bryndzove_halusky', name: 'Bryndzové halušky so slaninou', group: 'Hotové jedlá', kcal: 215, p: 7.2, c: 24.5, f: 9.8, portion: 350, portionName: '1 porcia (350g)' },
            { id: 'slepací_vyvar', name: 'Slepačí vývar s mäsom a rezancami', group: 'Hotové jedlá', kcal: 42, p: 3.5, c: 4.0, f: 1.3, portion: 300, portionName: '1 tanier (300ml)' },
            { id: 'šošovicová_polievka', name: 'Šošovicová polievka (bez zápražky)', group: 'Hotové jedlá', kcal: 68, p: 4.2, c: 10.5, f: 1.0, portion: 300, portionName: '1 tanier (300ml)' }
        ];

        const MEAL_CATEGORIES = {
            ranajky: { title: 'Raňajky', icon: '🌅', badgeClass: 'bg-amber-50 text-amber-800 border-amber-200' },
            obed:    { title: 'Obed', icon: '☀️', badgeClass: 'bg-emerald-50 text-emerald-800 border-emerald-200' },
            vecera:  { title: 'Večera', icon: '🌙', badgeClass: 'bg-indigo-50 text-indigo-800 border-indigo-200' },
            snack:   { title: 'Snack / Desiaty', icon: '🍎', badgeClass: 'bg-rose-50 text-rose-800 border-rose-200' }
        };

        // ==========================================
        // 2. APLIKAČNÝ STAV (State)
        // ==========================================
        let state = {
            profile: {
                gender: 'male',       // 'male' | 'female'
                age: 30,
                height: 178,
                weight: 78,
                activity: 1.375,
                goal: 'lose',         // 'lose' | 'maintain' | 'gain'
                macroSplit: 'recommended'
            },
            targets: {
                bmr: 1760,
                tdee: 2420,
                kcal: 1936,
                p: 145,
                c: 194,
                f: 65,
                pPct: 30,
                cPct: 40,
                fPct: 30
            },
            selectedMealCat: 'ranajky',
            waterMl: 0,
            diary: [] // Pole objektov { id, category, name, grams, kcal, p, c, f }
        };

        // ==========================================
        // 3. INICIALIZÁCIA A LOCALSTORAGE
        // ==========================================
        window.addEventListener('DOMContentLoaded', () => {
            loadStateFromStorage();
            initUI();
            populateFoodSelect(FOOD_DATABASE);
            calculateTargets();
            renderDiary();
            updateWaterUI();
            lucide.createIcons();
        });

        function saveStateToStorage() {
            try {
                localStorage.setItem('nutriplan_sk_state_v1', JSON.stringify({
                    profile: state.profile,
                    diary: state.diary,
                    waterMl: state.waterMl
                }));
            } catch (e) {
                console.warn('Nepodarilo sa uložiť stav do localStorage:', e);
            }
        }

        function loadStateFromStorage() {
            try {
                const raw = localStorage.getItem('nutriplan_sk_state_v1');
                if (raw) {
                    const parsed = JSON.parse(raw);
                    if (parsed.profile) state.profile = { ...state.profile, ...parsed.profile };
                    if (Array.isArray(parsed.diary)) state.diary = parsed.diary;
                    if (typeof parsed.waterMl === 'number') state.waterMl = parsed.waterMl;
                } else {
                    // Predvolený vzorový záznam na začiatok, aby používateľ hneď videl ako grafy fungujú
                    state.diary = [
                        { id: 'init_1', category: 'ranajky', name: 'Ovsené vločky', grams: 60, kcal: 225, p: 8.1, c: 36.0, f: 4.2 },
                        { id: 'init_2', category: 'ranajky', name: 'Grécky jogurt biely (0% tuku)', grams: 140, kcal: 80, p: 14.4, c: 5.6, f: 0.3 },
                        { id: 'init_3', category: 'ranajky', name: 'Čučoriedky / Lesné ovocie', grams: 80, kcal: 46, p: 0.6, c: 11.6, f: 0.2 }
                    ];
                }
            } catch (e) {
                console.warn('Chyba pri čítaní localStorage:', e);
            }
        }

        function initUI() {
            // Nastavenie hodnôt vo formulári podľa state.profile
            document.getElementById('input-age').value = state.profile.age;
            document.getElementById('range-age').value = state.profile.age;
            document.getElementById('input-height').value = state.profile.height;
            document.getElementById('range-height').value = state.profile.height;
            document.getElementById('input-weight').value = state.profile.weight;
            document.getElementById('range-weight').value = state.profile.weight;
            document.getElementById('select-activity').value = state.profile.activity;
            document.getElementById('select-macro-split').value = state.profile.macroSplit;

            updateGenderButtonsUI();
            updateGoalButtonsUI();
            selectMealCategory(state.selectedMealCat);
        }

        // ==========================================
        // 4. VÝPOČET BMR, TDEE A MAKROŽIVÍN
        // ==========================================
        function syncProfileInput(field, val) {
            const num = parseFloat(val);
            if (isNaN(num)) return;
            state.profile[field] = num;
            document.getElementById(`input-${field}`).value = num;
            document.getElementById(`range-${field}`).value = num;
            calculateTargets();
            updateWaterUI();
            saveStateToStorage();
        }

        function setGender(gender) {
            state.profile.gender = gender;
            updateGenderButtonsUI();
            calculateTargets();
            saveStateToStorage();
        }

        function updateGenderButtonsUI() {
            const btnMale = document.getElementById('btn-male');
            const btnFemale = document.getElementById('btn-female');
            if (state.profile.gender === 'male') {
                btnMale.className = 'flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl font-bold text-sm border-2 border-emerald-600 bg-emerald-50 text-emerald-800 transition-all shadow-2xs';
                btnFemale.className = 'flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl font-semibold text-sm border-2 border-slate-200 bg-white text-slate-600 hover:bg-slate-50 transition-all';
            } else {
                btnFemale.className = 'flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl font-bold text-sm border-2 border-emerald-600 bg-emerald-50 text-emerald-800 transition-all shadow-2xs';
                btnMale.className = 'flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl font-semibold text-sm border-2 border-slate-200 bg-white text-slate-600 hover:bg-slate-50 transition-all';
            }
        }

        function setGoal(goal) {
            state.profile.goal = goal;
            updateGoalButtonsUI();
            calculateTargets();
            saveStateToStorage();
        }

        function updateGoalButtonsUI() {
            const goals = ['lose', 'maintain', 'gain'];
            goals.forEach(g => {
                const btn = document.getElementById(`goal-${g}`);
                if (state.profile.goal === g) {
                    btn.className = 'flex flex-col items-center justify-center p-3 rounded-xl border-2 border-emerald-600 bg-emerald-50 text-emerald-900 text-center transition-all shadow-2xs';
                } else {
                    btn.className = 'flex flex-col items-center justify-center p-3 rounded-xl border-2 border-slate-200 bg-white text-slate-600 hover:bg-slate-50 text-center transition-all';
                }
            });
        }

        function updateProfile() {
            state.profile.activity = parseFloat(document.getElementById('select-activity').value);
            state.profile.macroSplit = document.getElementById('select-macro-split').value;
            calculateTargets();
            saveStateToStorage();
        }

        function calculateTargets() {
            const { gender, age, height, weight, activity, goal, macroSplit } = state.profile;

            // 1. Mifflin-St Jeor rovnica pre BMR
            let bmr = (10 * weight) + (6.25 * height) - (5 * age);
            bmr += (gender === 'male') ? 5 : -161;
            bmr = Math.round(bmr);

            // 2. TDEE (Celkový denný energetický výdaj)
            const tdee = Math.round(bmr * activity);

            // 3. Cieľové kalórie podľa cieľa
            let targetKcal = tdee;
            if (goal === 'lose') {
                targetKcal = Math.round(tdee * 0.80); // 20% kalorický deficit
            } else if (goal === 'gain') {
                targetKcal = Math.round(tdee * 1.15); // 15% kalorický nadbytok
            }

            // Bezpečnostné minimum
            const minSafe = (gender === 'male') ? 1400 : 1200;
            if (targetKcal < minSafe) targetKcal = minSafe;

            // 4. Rozloženie makroživín (Bielkoviny, Sacharidy, Tuky v %)
            let pPct = 30, cPct = 40, fPct = 30;

            if (macroSplit === 'recommended') {
                if (goal === 'lose') {
                    pPct = 32; cPct = 38; fPct = 30; // Vyššie bielkoviny na ochranu svalov v deficite
                } else if (goal === 'maintain') {
                    pPct = 25; cPct = 45; fPct = 30;
                } else if (goal === 'gain') {
                    pPct = 25; cPct = 50; fPct = 25; // Viac sacharidov na energiu a rast
                }
            } else if (macroSplit === 'balanced') {
                pPct = 25; cPct = 50; fPct = 25;
            } else if (macroSplit === 'highprotein') {
                pPct = 35; cPct = 40; fPct = 25;
            } else if (macroSplit === 'lowcarb') {
                pPct = 35; cPct = 20; fPct = 45;
            }

            // 5. Prepočet na gramy (1g B = 4 kcal, 1g S = 4 kcal, 1g T = 9 kcal)
            const pKcal = Math.round(targetKcal * (pPct / 100));
            const cKcal = Math.round(targetKcal * (cPct / 100));
            const fKcal = Math.round(targetKcal * (fPct / 100));

            const pGrams = Math.round(pKcal / 4);
            const cGrams = Math.round(cKcal / 4);
            const fGrams = Math.round(fKcal / 9);

            state.targets = {
                bmr,
                tdee,
                kcal: targetKcal,
                p: pGrams,
                c: cGrams,
                f: fGrams,
                pPct,
                cPct,
                fPct
            };

            // 6. Výpočet BMI
            const heightM = height / 100;
            const bmi = (weight / (heightM * heightM)).toFixed(1);
            let bmiText = 'Norma';
            let bmiClass = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30';
            if (bmi < 18.5) {
                bmiText = 'Podváha';
                bmiClass = 'bg-sky-500/20 text-sky-300 border-sky-500/30';
            } else if (bmi >= 25 && bmi < 30) {
                bmiText = 'Nadváha';
                bmiClass = 'bg-amber-500/20 text-amber-300 border-amber-500/30';
            } else if (bmi >= 30) {
                bmiText = 'Obezita';
                bmiClass = 'bg-rose-500/20 text-rose-300 border-rose-500/30';
            }

            // Vykreslenie výsledkov v ľavom paneli
            document.getElementById('res-bmr').textContent = bmr.toLocaleString('sk-SK');
            document.getElementById('res-tdee').textContent = tdee.toLocaleString('sk-SK');
            document.getElementById('res-target').textContent = targetKcal.toLocaleString('sk-SK');

            document.getElementById('macro-ratio-badge').textContent = `${pPct}% / ${cPct}% / ${fPct}%`;

            document.getElementById('res-p-pct').textContent = `${pPct}%`;
            document.getElementById('res-p-grams').textContent = pGrams;
            document.getElementById('res-p-kcal').textContent = pGrams * 4;

            document.getElementById('res-c-pct').textContent = `${cPct}%`;
            document.getElementById('res-c-grams').textContent = cGrams;
            document.getElementById('res-c-kcal').textContent = cGrams * 4;

            document.getElementById('res-f-pct').textContent = `${fPct}%`;
            document.getElementById('res-f-grams').textContent = fGrams;
            document.getElementById('res-f-kcal').textContent = fGrams * 9;

            const bmiBadge = document.getElementById('bmi-badge');
            bmiBadge.textContent = `BMI: ${bmi} (${bmiText})`;
            bmiBadge.className = `text-xs font-semibold px-2.5 py-1 rounded-full border ${bmiClass}`;

            // Aktualizácia progres grafov vpravo
            updateDashboardProgress();
        }

        // ==========================================
        // 5. AKTUALIZÁCIA GRAFOV A UKAZOVATEĽOV
        // ==========================================
        function updateDashboardProgress() {
            const totals = state.diary.reduce((acc, item) => {
                acc.kcal += item.kcal;
                acc.p += item.p;
                acc.c += item.c;
                acc.f += item.f;
                return acc;
            }, { kcal: 0, p: 0, c: 0, f: 0 });

            const eatenKcal = Math.round(totals.kcal);
            const eatenP = Math.round(totals.p);
            const eatenC = Math.round(totals.c);
            const eatenF = Math.round(totals.f);

            const targetKcal = state.targets.kcal;
            const remainingKcal = targetKcal - eatenKcal;
            const pctKcal = targetKcal > 0 ? Math.round((eatenKcal / targetKcal) * 100) : 0;

            // Kruhový graf (SVG r=66 => obvod = 2 * PI * 66 = 414.69)
            const circumference = 414.69;
            const clampedRatio = Math.min(Math.max(eatenKcal / targetKcal, 0), 1);
            const offset = circumference - (clampedRatio * circumference);
            const ringEl = document.getElementById('calorie-ring');
            ringEl.style.strokeDashoffset = offset;

            const ringLabel = document.getElementById('ring-label');
            const ringMainVal = document.getElementById('ring-main-value');
            const statusPill = document.getElementById('status-pill');

            if (remainingKcal >= 0) {
                ringLabel.textContent = 'Zostáva prijať';
                ringLabel.className = 'text-[11px] font-bold uppercase tracking-wider text-slate-400';
                ringMainVal.textContent = remainingKcal.toLocaleString('sk-SK');
                ringMainVal.className = 'text-3xl font-black text-slate-900 tracking-tight my-0.5';
                ringEl.style.stroke = '#10b981'; // Emerald

                if (pctKcal >= 90 && pctKcal <= 105) {
                    statusPill.textContent = 'Cieľ takmer splnený!';
                    statusPill.className = 'text-xs font-semibold px-3 py-1 rounded-full bg-emerald-100 text-emerald-800';
                } else {
                    statusPill.textContent = `Zostáva ${remainingKcal} kcal`;
                    statusPill.className = 'text-xs font-semibold px-3 py-1 rounded-full bg-slate-100 text-slate-700';
                }
            } else {
                const over = Math.abs(remainingKcal);
                ringLabel.textContent = 'Prekročené o';
                ringLabel.className = 'text-[11px] font-bold uppercase tracking-wider text-rose-500';
                ringMainVal.textContent = `+${over.toLocaleString('sk-SK')}`;
                ringMainVal.className = 'text-3xl font-black text-rose-600 tracking-tight my-0.5';
                ringEl.style.stroke = '#f43f5e'; // Rose

                statusPill.textContent = `Prekročený limit o ${over} kcal`;
                statusPill.className = 'text-xs font-semibold px-3 py-1 rounded-full bg-rose-100 text-rose-700';
            }

            document.getElementById('ring-target-value').textContent = targetKcal.toLocaleString('sk-SK');
            document.getElementById('eaten-kcal').textContent = eatenKcal.toLocaleString('sk-SK');
            document.getElementById('eaten-pct').textContent = pctKcal;

            // Makro bary
            updateSingleMacroBar('p', eatenP, state.targets.p, 'bg-blue-500', 'bg-rose-500');
            updateSingleMacroBar('c', eatenC, state.targets.c, 'bg-amber-500', 'bg-rose-500');
            updateSingleMacroBar('f', eatenF, state.targets.f, 'bg-rose-500', 'bg-rose-700');

            // Skutočný pomer prijatých makier
            const totalMacroKcal = (eatenP * 4) + (eatenC * 4) + (eatenF * 9);
            if (totalMacroKcal > 0) {
                const actP = Math.round(((eatenP * 4) / totalMacroKcal) * 100);
                const actC = Math.round(((eatenC * 4) / totalMacroKcal) * 100);
                const actF = Math.max(0, 100 - actP - actC);

                document.getElementById('actual-macro-split-text').textContent = `${actP}% B / ${actC}% S / ${actF}% T`;
                document.getElementById('split-bar-p').style.width = `${actP}%`;
                document.getElementById('split-bar-c').style.width = `${actC}%`;
                document.getElementById('split-bar-f').style.width = `${actF}%`;
            } else {
                document.getElementById('actual-macro-split-text').textContent = '0% B / 0% S / 0% T';
                document.getElementById('split-bar-p').style.width = '0%';
                document.getElementById('split-bar-c').style.width = '0%';
                document.getElementById('split-bar-f').style.width = '0%';
            }
        }

        function updateSingleMacroBar(key, eaten, goal, normalColorClass, overColorClass) {
            document.getElementById(`eaten-${key}`).textContent = eaten;
            document.getElementById(`goal-${key}`).textContent = goal;

            const diffEl = document.getElementById(`diff-${key}`);
            const diff = goal - eaten;
            if (diff >= 0) {
                diffEl.textContent = `(zostáva ${diff} g)`;
                diffEl.className = 'ml-1.5 text-[11px] text-slate-400';
            } else {
                diffEl.textContent = `(+${Math.abs(diff)} g nad cieľ)`;
                diffEl.className = 'ml-1.5 text-[11px] text-rose-500 font-semibold';
            }

            const pct = goal > 0 ? Math.min((eaten / goal) * 100, 100) : 0;
            const barEl = document.getElementById(`bar-${key}`);
            barEl.style.width = `${pct}%`;
            barEl.className = `${eaten > goal * 1.1 ? overColorClass : normalColorClass} h-full rounded-full transition-all duration-500`;
        }

        // ==========================================
        // 6. VÝBER A PRIDÁVANIE POTRAVÍN
        // ==========================================
        function switchFoodTab(tab) {
            const tabDb = document.getElementById('tab-db');
            const tabCustom = document.getElementById('tab-custom');
            const panelDb = document.getElementById('panel-db');
            const panelCustom = document.getElementById('panel-custom');

            if (tab === 'db') {
                tabDb.className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition-all bg-white text-slate-900 shadow-sm';
                tabCustom.className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition-all text-slate-600 hover:text-slate-900';
                panelDb.classList.remove('hidden');
                panelCustom.classList.add('hidden');
            } else {
                tabCustom.className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition-all bg-white text-slate-900 shadow-sm';
                tabDb.className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition-all text-slate-600 hover:text-slate-900';
                panelCustom.classList.remove('hidden');
                panelDb.classList.add('hidden');
            }
        }

        function selectMealCategory(cat) {
            state.selectedMealCat = cat;
            Object.keys(MEAL_CATEGORIES).forEach(k => {
                const btn = document.getElementById(`cat-${k}`);
                if (k === cat) {
                    btn.className = 'meal-cat-btn flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl text-xs font-bold border-2 border-emerald-600 bg-emerald-50 text-emerald-900 transition-all shadow-2xs';
                } else {
                    btn.className = 'meal-cat-btn flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl text-xs font-semibold border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 transition-all';
                }
            });
        }

        function populateFoodSelect(items) {
            const select = document.getElementById('food-select');
            select.innerHTML = '';

            if (items.length === 0) {
                const opt = document.createElement('option');
                opt.value = '';
                opt.textContent = 'Žiadna zhoda – skúste iný výraz alebo Vlastné hodnoty';
                select.appendChild(opt);
                updateDbFoodPreview();
                return;
            }

            // Zoskupenie podľa kategórií (optgroup)
            const groups = {};
            items.forEach(item => {
                if (!groups[item.group]) groups[item.group] = [];
                groups[item.group].push(item);
            });

            Object.keys(groups).forEach(groupName => {
                const optgroup = document.createElement('optgroup');
                optgroup.label = groupName;
                groups[groupName].forEach(food => {
                    const opt = document.createElement('option');
                    opt.value = food.id;
                    opt.textContent = `${food.name} (${food.kcal} kcal / 100g)`;
                    optgroup.appendChild(opt);
                });
                select.appendChild(optgroup);
            });

            onFoodSelectChange();
        }

        function filterFoodDatabase() {
            const query = document.getElementById('food-search').value.trim().toLowerCase();
            // Normalizácia diakritiky pre pohodlné vyhľadávanie
            const normalize = str => str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
            const normQuery = normalize(query);

            const filtered = FOOD_DATABASE.filter(f => 
                normalize(f.name).includes(normQuery) || normalize(f.group).includes(normQuery)
            );
            populateFoodSelect(filtered);
        }

        function getSelectedDbFoodObject() {
            const id = document.getElementById('food-select').value;
            return FOOD_DATABASE.find(f => f.id === id) || null;
        }

        function onFoodSelectChange() {
            const food = getSelectedDbFoodObject();
            const portionBtn = document.getElementById('btn-portion-default');
            if (food) {
                document.getElementById('food-grams').value = food.portion || 100;
                portionBtn.textContent = food.portionName || `Porcia (${food.portion}g)`;
                portionBtn.classList.remove('hidden');
            } else {
                portionBtn.classList.add('hidden');
            }
            updateDbFoodPreview();
        }

        function setQuickGrams(val) {
            const food = getSelectedDbFoodObject();
            if (val === 'portion' && food) {
                document.getElementById('food-grams').value = food.portion;
            } else if (typeof val === 'number') {
                document.getElementById('food-grams').value = val;
            }
            updateDbFoodPreview();
        }

        function updateDbFoodPreview() {
            const food = getSelectedDbFoodObject();
            const grams = parseFloat(document.getElementById('food-grams').value) || 0;

            if (!food || grams <= 0) {
                document.getElementById('preview-kcal').textContent = '0';
                document.getElementById('preview-p').textContent = '0';
                document.getElementById('preview-c').textContent = '0';
                document.getElementById('preview-f').textContent = '0';
                return;
            }

            const ratio = grams / 100;
            document.getElementById('preview-kcal').textContent = Math.round(food.kcal * ratio);
            document.getElementById('preview-p').textContent = (food.p * ratio).toFixed(1);
            document.getElementById('preview-c').textContent = (food.c * ratio).toFixed(1);
            document.getElementById('preview-f').textContent = (food.f * ratio).toFixed(1);
        }

        function addSelectedDbFood() {
            const food = getSelectedDbFoodObject();
            const grams = parseFloat(document.getElementById('food-grams').value);

            if (!food) {
                showToast('Vyberte potravinu zo zoznamu.', 'error');
                return;
            }
            if (isNaN(grams) || grams <= 0) {
                showToast('Zadajte platnú hmotnosť v gramoch.', 'error');
                return;
            }

            const ratio = grams / 100;
            const entry = {
                id: 'item_' + Date.now() + '_' + Math.random().toString(36).substring(2, 6),
                category: state.selectedMealCat,
                name: food.name,
                grams: Math.round(grams),
                kcal: Math.round(food.kcal * ratio),
                p: parseFloat((food.p * ratio).toFixed(1)),
                c: parseFloat((food.c * ratio).toFixed(1)),
                f: parseFloat((food.f * ratio).toFixed(1))
            };

            state.diary.push(entry);
            saveStateToStorage();
            renderDiary();
            updateDashboardProgress();
            showToast(`Pridané: ${entry.name} (${entry.grams}g)`);
        }

        function autoCalcCustomKcal() {
            const p = parseFloat(document.getElementById('custom-p').value) || 0;
            const c = parseFloat(document.getElementById('custom-c').value) || 0;
            const f = parseFloat(document.getElementById('custom-f').value) || 0;
            const kcal = Math.round((p * 4) + (c * 4) + (f * 9));
            document.getElementById('custom-kcal').value = kcal;
        }

        function addCustomFood() {
            const nameInput = document.getElementById('custom-name');
            const name = nameInput.value.trim();
            const grams = parseFloat(document.getElementById('custom-grams').value) || 100;
            const p = parseFloat(document.getElementById('custom-p').value) || 0;
            const c = parseFloat(document.getElementById('custom-c').value) || 0;
            const f = parseFloat(document.getElementById('custom-f').value) || 0;
            const kcal = parseFloat(document.getElementById('custom-kcal').value) || 0;

            if (!name) {
                showToast('Zadajte názov vlastného jedla.', 'error');
                nameInput.focus();
                return;
            }

            const entry = {
                id: 'custom_' + Date.now(),
                category: state.selectedMealCat,
                name: name,
                grams: Math.round(grams),
                kcal: Math.round(kcal),
                p: parseFloat(p.toFixed(1)),
                c: parseFloat(c.toFixed(1)),
                f: parseFloat(f.toFixed(1))
            };

            state.diary.push(entry);
            nameInput.value = '';
            saveStateToStorage();
            renderDiary();
            updateDashboardProgress();
            showToast(`Pridané vlastné jedlo: ${entry.name}`);
        }

        // ==========================================
        // 7. VYKRESLENIE DENNÍKA STRAVY
        // ==========================================
        function renderDiary() {
            const container = document.getElementById('diary-sections-container');
            container.innerHTML = '';

            document.getElementById('diary-count-badge').textContent = `${state.diary.length} ${state.diary.length === 1 ? 'položka' : (state.diary.length >= 2 && state.diary.length <= 4 ? 'položky' : 'položiek')}`;

            if (state.diary.length === 0) {
                container.innerHTML = `
                    <div class="text-center py-10 px-4 border-2 border-dashed border-slate-200 rounded-2xl bg-slate-50/50">
                        <div class="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-3">
                            <i data-lucide="utensils-crossed" class="w-6 h-6"></i>
                        </div>
                        <p class="text-sm font-bold text-slate-700">Váš dnešný denník je zatiaľ prázdny</p>
                        <p class="text-xs text-slate-500 mt-1 max-w-md mx-auto">Vyberte si potravinu zo zoznamu vyššie alebo kliknite na tlačidlo <strong>„Ukážkový deň“</strong> v pravom hornom rohu pre načítanie vzorového jedálnička.</p>
                    </div>
                `;
                lucide.createIcons();
                return;
            }

            Object.keys(MEAL_CATEGORIES).forEach(catKey => {
                const catMeta = MEAL_CATEGORIES[catKey];
                const items = state.diary.filter(item => item.category === catKey);

                if (items.length === 0) return;

                const catTotals = items.reduce((acc, i) => {
                    acc.kcal += i.kcal;
                    acc.p += i.p;
                    acc.c += i.c;
                    acc.f += i.f;
                    return acc;
                }, { kcal: 0, p: 0, c: 0, f: 0 });

                const sectionEl = document.createElement('div');
                sectionEl.className = 'border border-slate-200 rounded-xl overflow-hidden';

                let rowsHtml = items.map(item => `
                    <div class="flex items-center justify-between gap-3 p-3 bg-white hover:bg-slate-50/80 transition-colors border-t border-slate-100">
                        <div class="min-w-0 flex-1">
                            <div class="text-sm font-semibold text-slate-900 truncate">${escapeHtml(item.name)}</div>
                            <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-slate-500 mt-0.5">
                                <span class="font-medium text-slate-600">${item.grams} g</span>
                                <span class="text-blue-600 font-medium">B: ${item.p}g</span>
                                <span class="text-amber-600 font-medium">S: ${item.c}g</span>
                                <span class="text-rose-600 font-medium">T: ${item.f}g</span>
                            </div>
                        </div>
                        <div class="flex items-center gap-3 shrink-0">
                            <span class="text-sm font-extrabold text-slate-900">${item.kcal} <span class="text-xs font-normal text-slate-500">kcal</span></span>
                            <button onclick="removeDiaryItem('${item.id}')" class="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors" title="Odstrániť položku">
                                <i data-lucide="x" class="w-4 h-4"></i>
                            </button>
                        </div>
                    </div>
                `).join('');

                sectionEl.innerHTML = `
                    <div class="bg-slate-50 px-4 py-2.5 flex flex-wrap items-center justify-between gap-2">
                        <div class="flex items-center gap-2">
                            <span class="text-base">${catMeta.icon}</span>
                            <h4 class="text-sm font-bold text-slate-900">${catMeta.title}</h4>
                            <span class="text-[11px] font-semibold text-slate-400">(${items.length})</span>
                        </div>
                        <div class="flex items-center gap-3 text-xs">
                            <span class="text-slate-500 hidden sm:inline">B: <strong>${Math.round(catTotals.p)}g</strong> · S: <strong>${Math.round(catTotals.c)}g</strong> · T: <strong>${Math.round(catTotals.f)}g</strong></span>
                            <span class="font-extrabold text-emerald-700 bg-emerald-50 border border-emerald-200/60 px-2.5 py-0.5 rounded-full">${Math.round(catTotals.kcal)} kcal</span>
                        </div>
                    </div>
                    <div>
                        ${rowsHtml}
                    </div>
                `;

                container.appendChild(sectionEl);
            });

            lucide.createIcons();
        }

        function removeDiaryItem(id) {
            state.diary = state.diary.filter(item => item.id !== id);
            saveStateToStorage();
            renderDiary();
            updateDashboardProgress();
            showToast('Položka bola odstránená.');
        }

        // ==========================================
        // 8. UKÁŽKOVÝ DEŇ A VYČISTENIE DENNÍKA
        // ==========================================
        function loadDemoDay() {
            state.diary = [
                { id: 'demo_1', category: 'ranajky', name: 'Ovsené vločky', grams: 60, kcal: 225, p: 8.1, c: 36.0, f: 4.2 },
                { id: 'demo_2', category: 'ranajky', name: 'Skyr biely natur', grams: 140, kcal: 88, p: 15.4, c: 5.6, f: 0.3 },
                { id: 'demo_3', category: 'ranajky', name: 'Banán', grams: 120, kcal: 107, p: 1.3, c: 27.4, f: 0.4 },
                { id: 'demo_4', category: 'ranajky', name: 'Mandle / Vlašské orechy', grams: 20, kcal: 118, p: 4.2, c: 3.8, f: 10.4 },
                
                { id: 'demo_5', category: 'obed', name: 'Slepačí vývar s mäsom a rezancami', grams: 300, kcal: 126, p: 10.5, c: 12.0, f: 3.9 },
                { id: 'demo_6', category: 'obed', name: 'Kuracie prsia (surové)', grams: 160, kcal: 176, p: 37.0, c: 0.0, f: 1.9 },
                { id: 'demo_7', category: 'obed', name: 'Ryža biela / jazmínová (varená)', grams: 200, kcal: 260, p: 5.4, c: 56.4, f: 0.6 },
                { id: 'demo_8', category: 'obed', name: 'Olivový olej (Extra Virgin)', grams: 10, kcal: 88, p: 0.0, c: 0.0, f: 10.0 },

                { id: 'demo_9', category: 'snack', name: 'Srvátkový proteín (Whey 80%)', grams: 30, kcal: 116, p: 23.4, c: 2.0, f: 1.7 },
                { id: 'demo_10', category: 'snack', name: 'Jablko', grams: 150, kcal: 78, p: 0.5, c: 20.7, f: 0.3 },

                { id: 'demo_11', category: 'vecera', name: 'Losos (filet)', grams: 150, kcal: 312, p: 30.6, c: 0.0, f: 20.1 },
                { id: 'demo_12', category: 'vecera', name: 'Zemiaky varené v šupke', grams: 200, kcal: 154, p: 4.0, c: 34.0, f: 0.2 },
                { id: 'demo_13', category: 'vecera', name: 'Čerstvá zelenina (paradajka, paprika, uhorka)', grams: 150, kcal: 33, p: 1.4, c: 6.3, f: 0.3 }
            ];
            state.waterMl = 2000;
            saveStateToStorage();
            renderDiary();
            updateDashboardProgress();
            updateWaterUI();
            showToast('Ukážkový celodenný jedálniček bol načítaný!');
        }

        function confirmResetDiary() {
            if (state.diary.length === 0) {
                showToast('Denník je už prázdny.');
                return;
            }
            const modal = document.getElementById('confirm-modal');
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }

        function closeConfirmModal() {
            const modal = document.getElementById('confirm-modal');
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }

        function executeResetDiary() {
            state.diary = [];
            saveStateToStorage();
            renderDiary();
            updateDashboardProgress();
            closeConfirmModal();
            showToast('Denník stravy bol vymazaný.');
        }

        // ==========================================
        // 9. PITNÝ REŽIM
        // ==========================================
        function addWater(ml) {
            state.waterMl += ml;
            saveStateToStorage();
            updateWaterUI();
            showToast(`Pridaných +${ml} ml vody 💧`);
        }

        function resetWater() {
            state.waterMl = 0;
            saveStateToStorage();
            updateWaterUI();
        }

        function updateWaterUI() {
            // Odporúčanie: cca 35 ml na 1 kg hmotnosti
            const goalLiters = ((state.profile.weight * 35) / 1000).toFixed(1);
            const currentLiters = (state.waterMl / 1000).toFixed(2);
            const pct = Math.min((currentLiters / goalLiters) * 100, 100);

            document.getElementById('water-target-text').textContent = `${goalLiters} l`;
            document.getElementById('water-goal-num').textContent = goalLiters;
            document.getElementById('water-current-text').textContent = currentLiters;
            document.getElementById('water-progress-bar').style.width = `${pct}%`;
        }

        // ==========================================
        // 10. POMOCNÉ FUNKCIE (Toast, Escape HTML)
        // ==========================================
        function showToast(message, type = 'success') {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            const bgClass = type === 'error' ? 'bg-rose-600' : 'bg-slate-900';

            toast.className = `${bgClass} text-white px-4 py-2.5 rounded-xl shadow-lg text-xs sm:text-sm font-medium flex items-center gap-2 transition-all duration-300 opacity-0 translate-y-2`;
            toast.innerHTML = `
                <span>${type === 'error' ? '⚠️' : '✅'}</span>
                <span>${escapeHtml(message)}</span>
            `;

            container.appendChild(toast);
            requestAnimationFrame(() => {
                toast.classList.remove('opacity-0', 'translate-y-2');
            });

            setTimeout(() => {
                toast.classList.add('opacity-0', 'translate-y-2');
                setTimeout(() => toast.remove(), 300);
            }, 2600);
        }

        function escapeHtml(str) {
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#039;');
        }
    </script>
</body>
</html>
```

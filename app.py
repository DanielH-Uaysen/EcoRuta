import os
import json
import webbrowser
import threading
from flask import Flask, Response

# ========================================================
# 1. BASE DE DATOS 
# ========================================================
puntos_base = [
    # PUNTOS LIMPIOS (Color: blue)
    {"tipo": "Punto Limpio", "nombre": "Punto Limpio Los Cipreses", "lat": -45.583406, "lng": -72.055866, "color": "blue", "icono": "trash", "descripcion": "Ubicado en calle Los Cipreses con Los Liles.", "residuos": "Botellas de plástico, botellas de vidrio y latas de aluminio.", "detalle": "Botellas PET (agua, jugos - sin líquido y aplastadas), botellas y frascos de vidrio (no espejos ni loza), latas de aluminio (bebidas, cerveza - enjuagadas).", "no_reciclar": "Plásticos de un solo uso (bolsas, envases de snacks), latas de conservas (hojalata), vidrios rotos, espejos, loza, tazas o cerámica.", "horario": "24 hrs del día"},
    {"tipo": "Punto Limpio", "nombre": "Punto Limpio Terminal", "lat": -45.581670, "lng": -72.078009, "color": "blue", "icono": "trash", "descripcion": "Ubicado al lado del Terminal de Buses.", "residuos": "Botellas de plástico, botellas de vidrio y latas de aluminio.", "detalle": "Botellas PET (agua, jugos - sin líquido y aplastadas), botellas y frascos de vidrio (no espejos ni loza), latas de aluminio (bebidas, cerveza - enjuagadas).", "no_reciclar": "Plásticos de un solo uso (bolsas, envases de snacks), latas de conservas (hojalata), vidrios rotos, espejos, loza, tazas o cerámica.", "horario": "24 hrs del día"},
    {"tipo": "Punto Limpio", "nombre": "Punto Limpio Estancia Austral", "lat": -45.590734, "lng": -72.075897, "color": "blue", "icono": "trash", "descripcion": "Ubicado en Socovesa al lado de Poniente Uno.", "residuos": "Botellas de plástico, botellas de vidrio y latas de aluminio.", "detalle": "Botellas PET (agua, jugos - sin líquido y aplastadas), botellas y frascos de vidrio (no espejos ni loza), latas de aluminio (bebidas, cerveza - enjuagadas).", "no_reciclar": "Plásticos de un solo uso (bolsas, envases de snacks), latas de conservas (hojalata), vidrios rotos, espejos, loza, tazas o cerámica.", "horario": "24 hrs del día"},
    {"tipo": "Punto Limpio", "nombre": "Punto Limpio Bilbao", "lat": -45.577026, "lng": -72.054305, "color": "blue", "icono": "trash", "descripcion": "Ubicado en Francisco Bilbao enfrente del Colegio Alborada.", "residuos": "Botellas de plástico, botellas de vidrio y latas de aluminio.", "detalle": "Botellas PET (agua, jugos - sin líquido y aplastadas), botellas y frascos de vidrio (no espejos ni loza), latas de aluminio (bebidas, cerveza - enjuagadas).", "no_reciclar": "Plásticos de un solo uso (bolsas, envases de snacks), latas de conservas (hojalata), vidrios rotos, espejos, loza, tazas o cerámica.", "horario": "24 hrs del día"},
    {"tipo": "Punto Limpio", "nombre": "Punto Limpio Lillo", "lat": -45.578513, "lng": -72.070712, "color": "blue", "icono": "trash", "descripcion": "Ubicado en Eusebio Lillo pasando la calle Los Coihues.", "residuos": "Botellas de plástico, botellas de vidrio y latas de aluminio.", "detalle": "Botellas PET (agua, jugos - sin líquido y aplastadas), botellas y frascos de vidrio (no espejos ni loza), latas de aluminio (bebidas, cerveza - enjuagadas).", "no_reciclar": "Plásticos de un solo uso (bolsas, envases de snacks), latas de conservas (hojalata), vidrios rotos, espejos, loza, tazas o cerámica.", "horario": "24 hrs del día"},
    {"tipo": "Punto Limpio", "nombre": "Punto Limpio Ejército", "lat": -45.565573, "lng": -72.073026, "color": "blue", "icono": "trash", "descripcion": "Ubicado enfrente de la sede del Gobierno Regional cerca del estadio.", "residuos": "Botellas de plástico, botellas de vidrio y latas de aluminio.", "detalle": "Botellas PET (agua, jugos - sin líquido y aplastadas), botellas y frascos de vidrio (no espejos ni loza), latas de aluminio (bebidas, cerveza - enjuagadas).", "no_reciclar": "Plásticos de un solo uso (bolsas, envases de snacks), latas de conservas (hojalata), vidrios rotos, espejos, loza, tazas o cerámica.", "horario": "24 hrs del día"},
    {"tipo": "Punto Limpio", "nombre": "Punto Limpio Tejas Verdes", "lat": -45.567102, "lng": -72.028763, "color": "blue", "icono": "trash", "descripcion": "Punto de reciclaje sector Tejas Verdes.", "residuos": "Botellas de plástico, botellas de vidrio y latas de aluminio.", "detalle": "Botellas PET (agua, jugos - sin líquido y aplastadas), botellas y frascos de vidrio (no espejos ni loza), latas de aluminio (bebidas, cerveza - enjuagadas).", "no_reciclar": "Plásticos de un solo uso (bolsas, envases de snacks), latas de conservas (hojalata), vidrios rotos, espejos, loza, tazas o cerámica.", "horario": "24 hrs del día"},

    # PUNTOS LIMPIOS MÓVILES (Color: lightgreen)
    {"tipo": "Punto Limpio Móvil", "nombre": "Punto Limpio móvil Plaza Angol", "lat": -45.573159, "lng": -72.075314, "color": "lightgreen", "icono": "bottle-water", "descripcion": "Ubicado en Plaza Angol.", "residuos": "papel y cartón, latas de aluminio, Tetra Pak, y botellas plásticas", "detalle": "Papel y cartón (cajas, revistas, hojas secas), latas de bebidas, envases Tetra Pak (cajas de leche/jugo multicapa - desarmadas y enjuagadas), botellas PET.", "no_reciclar": "Papel higiénico, servilletas usadas, cartones manchados con grasa (como cajas de pizza), papeles plastificados o envases con restos de comida.", "horario": "lunes a viernes de 10:00 a 16:00 horas"},
    {"tipo": "Punto Limpio Móvil", "nombre": "Punto móvil Glaciar Nef", "lat": -45.571335, "lng": -72.033835, "color": "lightgreen", "icono": "bottle-water", "descripcion": "Ubicado en Glaciar Nef con Campos de Hielo.", "residuos": "papel y cartón, latas de aluminio, Tetra Pak, y botellas plásticas", "detalle": "Papel y cartón (cajas, revistas, hojas secas), latas de bebidas, envases Tetra Pak (cajas de leche/jugo multicapa - desarmadas y enjuagadas), botellas PET.", "no_reciclar": "Papel higiénico, servilletas usadas, cartones manchados con grasa (como cajas de pizza), papeles plastificados o envases con restos de comida.", "horario": "lunes a viernes de 10:00 a 16:00 horas"},
    {"tipo": "Punto Limpio Móvil", "nombre": "Punto móvil El Claro", "lat": -45.579046, "lng": -72.083359, "color": "lightgreen", "icono": "bottle-water", "descripcion": "Ubicado en el sector El Claro, cerca de la tolva municipal.", "residuos": "papel y cartón, latas de aluminio, Tetra Pak, y botellas plásticas", "detalle": "Papel y cartón (cajas, revistas, hojas secas), latas de bebidas, envases Tetra Pak (cajas de leche/jugo multicapa - desarmadas y enjuagadas), botellas PET.", "no_reciclar": "Papel higiénico, servilletas usadas, cartones manchados con grasa (como cajas de pizza), papeles plastificados o envases con restos de comida.", "horario": "lunes a viernes de 10:00 a 16:00 horas"},

    # RECICLAJES ESPECÍFICOS (Color: beige)
    {"tipo": "Reciclaje Específico", "nombre": "Vidrio (Sodimac)", "lat": -45.578619, "lng": -72.074394, "color": "beige", "icono": "glass", "descripcion": "Ubicado dentro de Homecenter Sodimac.", "residuos": "Objetos hechos de vidrio.", "detalle": "Envases de vidrio fundido como botellas de vino, cerveza o frascos de mermelada.", "no_reciclar": "Ampolletas, tubos fluorescentes, espejos, ventanas, parabrisas, loza, tazas, cerámica o cristal roto.", "horario": "Lunes a sábado de 08:30 a 20:30 hrs y los domingos de 09:00 a 20:30 hrs."},
    {"tipo": "Reciclaje Específico", "nombre": "Vidrio (Comercial San Cristóbal)", "lat": -45.581177, "lng": -72.041971, "color": "beige", "icono": "glass", "descripcion": "Ubicado dentro de Comercial San Cristóbal al final de Francisco Bilbao.", "residuos": "Objetos hechos de vidrio.", "detalle": "Envases de vidrio fundido como botellas de vino, cerveza o frascos de mermelada.", "no_reciclar": "Ampolletas, tubos fluorescentes, espejos, ventanas, parabrisas, loza, tazas, cerámica o cristal roto.", "horario": "Lunes a Jueves: 08:30 a 13:00 y 14:30 a 19:00. Viernes: 08:30 a 13:00 y 14:30 a 18:00 hrs."},
    {"tipo": "Reciclaje Específico", "nombre": "Pilas en desuso (Edelaysen)", "lat": -45.572639, "lng": -72.068782, "color": "beige", "icono": "flash", "descripcion": "Ubicado dentro del edificio de Edelaysen en Francisco Bilbao.", "residuos": "Pilas en desuso.", "detalle": "Pilas cilíndricas (AA, AAA, C, D), de 9V y de botón. Residuos con metales pesados peligrosos.", "no_reciclar": "Baterías de vehículos o motos, aparatos electrónicos enteros (se debe extraer la pila antes), baterías de celulares hinchadas.", "horario": "Lunes a viernes de 08:30 a 16:00 hrs."},
    {"tipo": "Reciclaje Específico", "nombre": "Patagonia sin Residuos", "lat": -45.563541, "lng": -71.954551, "color": "darkgreen", "icono": "trash", "descripcion": "Ubicado cerca del vertedero municipal.", "residuos": "Envases y Embalajes, Aceite Vegetal, Baterías Fuera de Uso, Aceite Lubricante Usado", "detalle": "Aceite de cocina usado (frío en botellas), baterías de vehículos (autos/motos), aceite de motor de combustión.", "no_reciclar": "Pilas domésticas comunes, basura domiciliaria, escombros de construcción.", "horario": "lunes a viernes de 10:00 a 13:00 hrs"},

    # VERTEDERO MUNICIPAL (Color: darkgreen)
    {"tipo": "Vertedero Municipal", "nombre": "Vertedero Municipal", "lat": -45.560895, "lng": -71.954933, "color": "darkgreen", "icono": "trash", "descripcion": "Ubicado camino a Coyhaique Alto.", "residuos": "Recibe basura domiciliaria y residuos sólidos asimilables.", "detalle": "Basura general del hogar que no cuenta con un canal de reciclaje habilitado.", "no_reciclar": "Residuos industriales peligrosos, químicos tóxicos, baterías de vehículos (sin declarar).", "horario": "Lunes a viernes de 08:00 a 20:00. Sábados y domingos de 09:00 a 17:00 hrs."},

    # TOLVAS (Color: orange)
    {"tipo": "Tolva", "nombre": "Tolva Cementerio", "lat": -45.571490, "lng": -72.056918, "color": "orange", "icono": "inbox", "descripcion": "Al lado del Cementerio y Baquedano.", "residuos": "Residuos voluminosos y escombros.", "detalle": "Voluminosos (colchones, sillones, electrodomésticos grandes) y escombros (restos menores de construcción, ladrillos, cerámicas).", "no_reciclar": "Bolsas de basura domiciliaria común, residuos peligrosos, neumáticos, restos biológicos o baterías.", "horario": "Martes y Jueves. 07:30 a 12:00 o hasta su llenado."},
    {"tipo": "Tolva", "nombre": "Tolva Cerro Negro", "lat": -45.585878, "lng": -72.021750, "color": "orange", "icono": "inbox", "descripcion": "Sector Cerro Negro, Coyhaique.", "residuos": "Residuos voluminosos y escombros.", "detalle": "Voluminosos (colchones, sillones, electrodomésticos grandes) y escombros (restos menores de construcción, ladrillos, cerámicas).", "no_reciclar": "Bolsas de basura domiciliaria común, residuos peligrosos, neumáticos, restos biológicos o baterías.", "horario": "Lunes, Miércoles y Viernes. 07:30 a 12:00 o hasta su llenado."},
    {"tipo": "Tolva", "nombre": "Tolva El Claro", "lat": -45.579109, "lng": -72.083785, "color": "orange", "icono": "inbox", "descripcion": "Sector El Claro, Coyhaique.", "residuos": "Residuos voluminosos y escombros.", "detalle": "Voluminosos (colchones, sillones, electrodomésticos grandes) y escombros (restos menores de construcción, ladrillos, cerámicas).", "no_reciclar": "Bolsas de basura domiciliaria común, residuos peligrosos, neumáticos, restos biológicos o baterías.", "horario": "Martes y Jueves. 07:30 a 12:00 o hasta su llenado."},
    {"tipo": "Tolva", "nombre": "Tolva El Salto Chico", "lat": -45.623862, "lng": -72.101854, "color": "orange", "icono": "inbox", "descripcion": "Sector El Salto Chico, Coyhaique.", "residuos": "Residuos voluminosos y escombros.", "detalle": "Voluminosos (colchones, sillones, electrodomésticos grandes) y escombros (restos menores de construcción, ladrillos, cerámicas).", "no_reciclar": "Bolsas de basura domiciliaria común, residuos peligrosos, neumáticos, restos biológicos o baterías.", "horario": "Martes y Jueves. 07:30 a 12:00 o hasta su llenado."},
    {"tipo": "Tolva", "nombre": "Tolva Tejas Verdes", "lat": -45.565400, "lng": -72.023274, "color": "orange", "icono": "inbox", "descripcion": "Sector Tejas Verdes, Coyhaique.", "residuos": "Residuos voluminosos y escombros.", "detalle": "Voluminosos (colchones, sillones, electrodomésticos grandes) y escombros (restos menores de construcción, ladrillos, cerámicas).", "no_reciclar": "Bolsas de basura domiciliaria común, residuos peligrosos, neumáticos, restos biológicos o baterías.", "horario": "Lunes, Miércoles y Viernes. 07:30 a 12:00 o hasta su llenado."},
    {"tipo": "Tolva", "nombre": "Tolva Coyhaique Alto", "lat": -45.570032, "lng": -72.014855, "color": "orange", "icono": "inbox", "descripcion": "Camino hacia Coyhaique Alto.", "residuos": "Residuos voluminosos y escombros.", "detalle": "Voluminosos (colchones, sillones, electrodomésticos grandes) y escombros (restos menores de construcción, ladrillos, cerámicas).", "no_reciclar": "Bolsas de basura domiciliaria común, residuos peligrosos, neumáticos, restos biológicos o baterías.", "horario": "Lunes, Miércoles y Viernes. 07:30 a 12:00 o hasta su llenado."}
]

ARCHIVO_BD = "puntos_coyhaique.json"


def cargar_puntos():
    if not os.path.exists(ARCHIVO_BD):
        with open(ARCHIVO_BD, "w", encoding="utf-8") as f:
            json.dump(puntos_base, f, indent=4)
        return puntos_base.copy()
    with open(ARCHIVO_BD, "r", encoding="utf-8") as f:
        return json.load(f)


# ========================================================
# 2. DASHBOARD (HTML + CSS + JS embebido)
# El estado Abierto/Cerrado se calcula EN VIVO en el navegador.
# ========================================================
HTML_DASHBOARD = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>EcoRuta · Dashboard de Reciclaje · Coyhaique</title>
    __ASSETS_HEAD__
    <style>
        :root {
            --azul: #1497CE; --azul-claro: #36B6E8; --azul-prof: #0A3D5E;
            --verde: #5FB330; --verde-osc: #4C9326;
            --amarillo: #F4C220; --naranja: #EE7B2F; --fucsia: #DD1A77;
            --crema: #FBF8F0; --tinta: #103A52; --gris: #6a8190;
            --panel: #ffffff; --fondo: #eef3f6;
        }
        * { box-sizing: border-box; }
        html, body { margin: 0; height: 100%; }
        body { font-family: 'Montserrat', sans-serif; color: var(--tinta); background: var(--fondo); overflow: hidden; }
        .app { display: grid; grid-template-rows: auto 1fr; height: 100vh; }

        /* ---------- HEADER ---------- */
        .topbar {
            display: flex; align-items: center; justify-content: space-between; gap: 16px;
            background: linear-gradient(100deg, var(--azul-prof) 0%, #0E5680 100%);
            color: #fff; padding: 12px 22px; box-shadow: 0 4px 18px rgba(0,0,0,0.18); z-index: 500;
        }
        .brand { display: flex; align-items: center; gap: 12px; }
        .brand .logo { width: 46px; height: 46px; flex-shrink: 0; }
        .brand .nombre { font-family: 'Baloo 2', cursive; font-weight: 800; font-size: 1.7rem; line-height: 1; }
        .brand .nombre .eco { color: var(--azul-claro); } .brand .nombre .ruta { color: #8fd95b; }
        .brand .sub { font-size: 0.72rem; color: #aacbe0; font-weight: 600; letter-spacing: 0.4px; margin-top: 2px; }
        .topbar-right { display: flex; align-items: center; gap: 22px; }
        .resumen-abiertos { text-align: right; }
        .resumen-abiertos .n { font-family: 'Baloo 2', cursive; font-weight: 800; font-size: 1.5rem; line-height: 1; }
        .resumen-abiertos .n b { color: #8fd95b; } .resumen-abiertos small { color: #aacbe0; font-size: 0.72rem; font-weight: 600; }
        .reloj { text-align: right; padding-left: 22px; border-left: 1px solid rgba(255,255,255,0.18); }
        .reloj .hora { font-family: 'Baloo 2', cursive; font-weight: 700; font-size: 1.35rem; line-height: 1; }
        .reloj .fecha { font-size: 0.72rem; color: #aacbe0; font-weight: 600; text-transform: capitalize; }

        /* ---------- CUERPO ---------- */
        .cuerpo { display: grid; grid-template-columns: 320px 1fr 250px; min-height: 0; }
        .sidebar { background: var(--panel); border-right: 1px solid #e3eaef; overflow-y: auto; padding: 18px; }
        .sidebar::-webkit-scrollbar { width: 7px; } .sidebar::-webkit-scrollbar-thumb { background: #d4dee4; border-radius: 10px; }

        .stats { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 22px; }
        .stat { border-radius: 16px; padding: 16px; color: #fff; position: relative; overflow: hidden; }
        .stat .v { font-family: 'Baloo 2', cursive; font-weight: 800; font-size: 2rem; line-height: 1; }
        .stat .l { font-size: 0.72rem; font-weight: 600; opacity: 0.92; margin-top: 4px; }
        .stat i { position: absolute; right: 10px; top: 10px; font-size: 1.5rem; opacity: 0.28; }
        .stat-total { background: linear-gradient(135deg, var(--azul), #0E6E9E); grid-column: span 2; }
        .stat-abiertos { background: linear-gradient(135deg, var(--verde), var(--verde-osc)); }
        .stat-cerrados { background: linear-gradient(135deg, #8794a0, #5d6b76); }

        .titulo-sec { font-family: 'Baloo 2', cursive; font-weight: 700; font-size: 1rem; color: var(--azul-prof); margin: 0 0 12px; display: flex; align-items: center; gap: 8px; }
        .titulo-sec i { color: var(--verde); }

        .filtros { display: flex; flex-direction: column; gap: 9px; margin-bottom: 22px; }
        .chip {
            display: flex; align-items: center; gap: 11px; padding: 11px 13px; border-radius: 13px;
            border: 1.5px solid #e6edf1; background: #fff; cursor: pointer; transition: all 0.18s ease; user-select: none;
        }
        .chip:hover { border-color: #cfe0e9; transform: translateX(2px); }
        .chip.off { opacity: 0.42; background: #f6f8f9; }
        .chip .punto { width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 0.72rem; flex-shrink: 0; }
        .chip .nom { font-weight: 600; font-size: 0.88rem; flex: 1; }
        .chip .cnt { font-weight: 700; font-size: 0.8rem; color: var(--gris); background: #eef3f6; border-radius: 999px; padding: 2px 9px; }
        .chip .check { color: var(--verde); font-size: 0.9rem; }
        .chip.off .check { color: #c3ccd2; }

        .nota { font-size: 0.74rem; color: var(--gris); line-height: 1.5; background: #f3f8f4; border-left: 3px solid var(--verde); padding: 10px 12px; border-radius: 8px; }

        /* ---------- PANEL DERECHO: CATEGORÍAS DE MATERIALES ---------- */
        .sidebar-der { border-right: none; border-left: 1px solid #e3eaef; }
        .mat-chip { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 12px; border: 1.5px solid #e6edf1; background: #fff; cursor: pointer; transition: all 0.18s ease; user-select: none; margin-bottom: 9px; }
        .mat-chip:hover { border-color: #cfe0e9; transform: translateX(-2px); }
        .mat-chip.activo { border-color: var(--verde); background: #f0f9ea; box-shadow: 0 2px 10px rgba(95,179,48,0.18); }
        .mat-chip .mi { width: 30px; height: 30px; border-radius: 9px; background: #eef5f9; color: var(--azul); display: flex; align-items: center; justify-content: center; font-size: 0.85rem; flex-shrink: 0; }
        .mat-chip.activo .mi { background: var(--verde); color: #fff; }
        .mat-chip .mn { font-weight: 600; font-size: 0.84rem; flex: 1; line-height: 1.2; }
        .mat-chip .mc { font-weight: 700; font-size: 0.76rem; color: var(--gris); background: #eef3f6; border-radius: 999px; padding: 2px 8px; }
        .btn-limpiar-mat { width: 100%; margin-top: 4px; padding: 10px; border: 1px dashed #c9d6de; border-radius: 10px; background: transparent; color: var(--gris); font-family: 'Montserrat', sans-serif; font-weight: 600; font-size: 0.8rem; cursor: pointer; display: none; }
        .btn-limpiar-mat:hover { color: var(--fucsia); border-color: var(--fucsia); }
        .btn-limpiar-mat.visible { display: block; }

        /* ---------- MAPA ---------- */
        .mapa-wrap { position: relative; min-height: 0; }
        #map { width: 100%; height: 100%; }
        .leaflet-container { font-family: 'Montserrat', sans-serif; }

        .custom-marker-pin { display: flex; justify-content: center; align-items: center; width: 34px; height: 34px; border-radius: 50% 50% 50% 0; color: #fff; transform: rotate(-45deg); box-shadow: 2px 2px 6px rgba(0,0,0,0.4); border: 2px solid #fff; }
        .custom-marker-pin i { transform: rotate(45deg); font-size: 14px; }
        .marker-cerrado { opacity: 0.5; filter: grayscale(0.4); }
        .estado-dot { position: absolute; top: -3px; right: -3px; width: 13px; height: 13px; border-radius: 50%; border: 2px solid #fff; }

        /* Popup */
        .popup-card { width: 220px; }
        .popup-card h5 { margin: 0 0 6px; font-family: 'Baloo 2', cursive; color: var(--azul-prof); font-size: 1.05rem; }
        .badge { display: inline-flex; align-items: center; gap: 6px; font-size: 0.74rem; font-weight: 700; padding: 3px 11px; border-radius: 999px; margin-bottom: 7px; }
        .badge::before { content: ''; width: 8px; height: 8px; border-radius: 50%; background: currentColor; }
        .b-abierto { background: #e8f5e9; color: #1b7a32; border: 1px solid #76c47e; }
        .b-cerrado { background: #ffebee; color: #c62828; border: 1px solid #ef9a9a; }
        .b-desconocido { background: #eef2f4; color: #5d6b76; border: 1px solid #c3ccd2; }
        .popup-card p { margin: 4px 0; font-size: 0.82rem; line-height: 1.35; color: #44606e; }
        .popup-btn { width: 100%; margin-top: 9px; padding: 9px; border: none; border-radius: 9px; background: linear-gradient(135deg, var(--verde), var(--verde-osc)); color: #fff; font-weight: 700; font-family: 'Montserrat', sans-serif; cursor: pointer; }

        /* ---------- DRAWER DETALLE ---------- */
        .drawer-overlay { position: fixed; inset: 0; background: rgba(8,30,46,0.35); opacity: 0; pointer-events: none; transition: opacity 0.25s; z-index: 900; }
        .drawer-overlay.open { opacity: 1; pointer-events: auto; }
        .drawer {
            position: fixed; top: 0; right: 0; height: 100%; width: 420px; max-width: 90vw; background: #fff;
            box-shadow: -12px 0 40px rgba(0,0,0,0.25); transform: translateX(100%); transition: transform 0.3s cubic-bezier(.2,.7,.2,1);
            z-index: 950; display: flex; flex-direction: column;
        }
        .drawer.open { transform: translateX(0); }
        .drawer-head { padding: 22px 24px 18px; color: #fff; position: relative; }
        .drawer-head .tipo { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; opacity: 0.9; }
        .drawer-head h2 { font-family: 'Baloo 2', cursive; font-weight: 800; font-size: 1.6rem; margin: 6px 0 10px; }
        .drawer-close { position: absolute; top: 18px; right: 18px; background: rgba(255,255,255,0.2); border: none; color: #fff; width: 34px; height: 34px; border-radius: 50%; cursor: pointer; font-size: 1rem; }
        .drawer-close:hover { background: rgba(255,255,255,0.35); }
        .drawer-body { padding: 22px 24px; overflow-y: auto; flex: 1; }
        .info-row { display: flex; gap: 13px; margin-bottom: 18px; align-items: flex-start; }
        .info-row .ic { width: 40px; height: 40px; border-radius: 11px; background: #f0f5f8; color: var(--azul); display: flex; align-items: center; justify-content: center; font-size: 1.05rem; flex-shrink: 0; }
        .info-row .lbl { font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; color: var(--gris); margin-bottom: 3px; }
        .info-row .txt { font-size: 0.95rem; line-height: 1.45; }
        .caja { border-radius: 12px; padding: 16px 18px; margin-top: 14px; }
        .caja .t { font-size: 0.78rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
        .caja p { margin: 0; font-size: 0.88rem; line-height: 1.55; }
        .caja-si { background: #eef8ee; border: 1px solid #cfeacf; } .caja-si .t { color: #1b7a32; } .caja-si p { color: #2f5d36; }
        .caja-no { background: #fdeeee; border: 1px solid #f5cccc; } .caja-no .t { color: #c62828; } .caja-no p { color: #7a3636; }
        .drawer-foot { padding: 16px 24px; border-top: 1px solid #eef2f4; }
        .btn-ruta { display: flex; align-items: center; justify-content: center; gap: 10px; width: 100%; padding: 14px; border-radius: 12px; background: linear-gradient(135deg, var(--azul), #0E6E9E); color: #fff; text-decoration: none; font-weight: 700; }
        .btn-ruta:hover { filter: brightness(1.06); }

        @media (max-width: 860px) {
            .cuerpo { grid-template-columns: 1fr; }
            .sidebar { display: none; }
        }
    </style>
</head>
<body>
<div class="app">
    <!-- HEADER -->
    <div class="topbar">
        <div class="brand">
            <svg class="logo" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <circle cx="50" cy="50" r="48" fill="#0E5680"/>
                <g transform="translate(50,58) scale(0.42)" fill="#F4C220">
                    <rect x="-44" y="40" width="9" height="40" rx="4"/><rect x="-30" y="42" width="9" height="38" rx="4"/>
                    <rect x="30" y="42" width="9" height="38" rx="4"/><rect x="44" y="40" width="9" height="40" rx="4"/>
                    <ellipse cx="0" cy="30" rx="50" ry="28"/><circle cx="-38" cy="26" r="26"/><circle cx="40" cy="28" r="22"/>
                    <path d="M-62,18 q-12,-2 -16,8 q10,2 16,-2 Z"/><path d="M40,12 L58,-30 L72,-26 L56,18 Z"/>
                    <ellipse cx="68" cy="-34" rx="17" ry="12" transform="rotate(-20 68 -34)"/>
                    <ellipse cx="84" cy="-26" rx="9" ry="6" transform="rotate(-20 84 -26)"/>
                    <path d="M58,-44 q-6,-10 2,-16 q6,4 5,14 Z"/>
                    <g stroke="#F4C220" stroke-width="5" stroke-linecap="round" fill="none">
                        <path d="M64,-46 L60,-70"/><path d="M60,-70 L50,-82"/><path d="M60,-70 L66,-86"/>
                        <path d="M72,-44 L76,-66"/><path d="M76,-66 L70,-80"/><path d="M76,-66 L86,-78"/>
                    </g>
                </g>
            </svg>
            <div>
                <div class="nombre"><span class="eco">Eco</span><span class="ruta">Ruta</span></div>
                <div class="sub">Dashboard de reciclaje · Coyhaique</div>
            </div>
        </div>
        <div class="topbar-right">
            <div class="resumen-abiertos">
                <div class="n"><b id="kpi-abiertos">–</b> / <span id="kpi-total">–</span></div>
                <small>puntos abiertos ahora</small>
            </div>
            <div class="reloj">
                <div class="hora" id="reloj-hora">--:--</div>
                <div class="fecha" id="reloj-fecha">—</div>
            </div>
        </div>
    </div>

    <!-- CUERPO -->
    <div class="cuerpo">
        <aside class="sidebar">
            <div class="stats">
                <div class="stat stat-total"><i class="fa-solid fa-recycle"></i><div class="v" id="s-total">0</div><div class="l">Puntos de reciclaje</div></div>
                <div class="stat stat-abiertos"><i class="fa-solid fa-door-open"></i><div class="v" id="s-abiertos">0</div><div class="l">Abiertos ahora</div></div>
                <div class="stat stat-cerrados"><i class="fa-solid fa-door-closed"></i><div class="v" id="s-cerrados">0</div><div class="l">Cerrados ahora</div></div>
            </div>

            <h3 class="titulo-sec"><i class="fa-solid fa-filter"></i> Filtrar por categoría</h3>
            <div class="filtros" id="filtros"></div>

            <h3 class="titulo-sec"><i class="fa-solid fa-circle-info"></i> Cómo usar</h3>
            <div class="nota">Haz clic en un punto del mapa para ver su ficha completa: qué reciclar, qué no, horario y si está abierto en este momento. Usa los filtros para mostrar u ocultar categorías.</div>
        </aside>

        <div class="mapa-wrap">
            <div id="map"></div>
        </div>

        <aside class="sidebar sidebar-der">
            <h3 class="titulo-sec"><i class="fa-solid fa-recycle"></i> Categorías</h3>
            <div class="nota" style="margin-bottom:14px;">Elige un material para ver en el mapa dónde puedes reciclarlo.</div>
            <div id="materiales"></div>
            <button class="btn-limpiar-mat" id="btn-limpiar-mat" onclick="limpiarMaterial()"><i class="fa-solid fa-xmark"></i> Quitar filtro de material</button>
        </aside>
    </div>
</div>

<!-- DRAWER DETALLE -->
<div class="drawer-overlay" id="overlay" onclick="cerrarDrawer()"></div>
<div class="drawer" id="drawer">
    <div class="drawer-head" id="drawer-head">
        <button class="drawer-close" onclick="cerrarDrawer()"><i class="fa-solid fa-xmark"></i></button>
        <div class="tipo" id="d-tipo">—</div>
        <h2 id="d-nombre">—</h2>
        <span class="badge" id="d-estado">—</span>
    </div>
    <div class="drawer-body">
        <div class="info-row">
            <div class="ic"><i class="fa-solid fa-map-location-dot"></i></div>
            <div><div class="lbl">Dirección</div><div class="txt" id="d-desc">—</div></div>
        </div>
        <div class="info-row">
            <div class="ic"><i class="fa-regular fa-clock"></i></div>
            <div><div class="lbl">Horario</div><div class="txt" id="d-horario">—</div></div>
        </div>
        <div class="caja caja-si">
            <div class="t"><i class="fa-solid fa-circle-check"></i> Qué se recicla aquí</div>
            <p id="d-si">—</p>
        </div>
        <div class="caja caja-no">
            <div class="t"><i class="fa-solid fa-ban"></i> Qué NO debes dejar</div>
            <p id="d-no">—</p>
        </div>
    </div>
    <div class="drawer-foot">
        <a class="btn-ruta" id="d-ruta" href="#" target="_blank" rel="noopener"><i class="fa-solid fa-diamond-turn-right"></i> Cómo llegar</a>
    </div>
</div>

<script>
    const PUNTOS = __PUNTOS_JSON__;

    const colorMap = { "blue": "#1e88e5", "lightgreen": "#8bc34a", "beige": "#ffb300", "orange": "#fb8c00", "darkgreen": "#2e7d32" };
    const iconMap = { "trash": "fa-solid fa-trash-can", "bottle-water": "fa-solid fa-bottle-water", "glass": "fa-solid fa-wine-bottle", "flash": "fa-solid fa-battery-three-quarters", "inbox": "fa-solid fa-dumpster" };
    const CATS = [
        { tipo: "Punto Limpio",        icono: "fa-solid fa-trash-can",    color: "#1e88e5" },
        { tipo: "Punto Limpio Móvil",  icono: "fa-solid fa-bottle-water", color: "#8bc34a" },
        { tipo: "Tolva",               icono: "fa-solid fa-dumpster",     color: "#fb8c00" },
        { tipo: "Reciclaje Específico",icono: "fa-solid fa-wine-bottle",  color: "#ffb300" },
        { tipo: "Vertedero Municipal", icono: "fa-solid fa-industry",     color: "#2e7d32" }
    ];

    /* ===== Categorías de materiales (panel derecho) =====
       Cada material se detecta buscando sus palabras clave en los campos
       "residuos" y "detalle" del punto (NO en "no_reciclar", para evitar
       falsos positivos con lo que está prohibido dejar). */
    const MATERIALES = [
        { id: "vidrio",   nombre: "Vidrio",                  icono: "fa-solid fa-wine-bottle",            claves: ["vidrio"] },
        { id: "plastico", nombre: "Plástico (botellas PET)", icono: "fa-solid fa-bottle-water",           claves: ["plástic", "pet"] },
        { id: "latas",    nombre: "Latas de aluminio",       icono: "fa-solid fa-jar",                    claves: ["latas"] },
        { id: "papel",    nombre: "Papel y cartón",          icono: "fa-solid fa-newspaper",              claves: ["papel", "cartón"] },
        { id: "tetra",    nombre: "Tetra Pak",               icono: "fa-solid fa-box",                    claves: ["tetra"] },
        { id: "pilas",    nombre: "Pilas",                   icono: "fa-solid fa-battery-three-quarters", claves: ["pilas"] },
        { id: "baterias", nombre: "Baterías de vehículos",   icono: "fa-solid fa-car-battery",            claves: ["baterías", "baterias"] },
        { id: "aceites",  nombre: "Aceites usados",          icono: "fa-solid fa-oil-can",                claves: ["aceite"] },
        { id: "volum",    nombre: "Voluminosos y escombros", icono: "fa-solid fa-couch",                  claves: ["voluminosos", "escombros"] },
        { id: "domic",    nombre: "Basura domiciliaria",     icono: "fa-solid fa-trash-can",              claves: ["domiciliaria"] }
    ];
    let materialActivo = null;

    function textoReciclable(p) {
        return ((p.residuos || "") + " " + (p.detalle || "")).toLowerCase();
    }
    function tieneMaterial(p, mat) {
        const t = textoReciclable(p);
        return mat.claves.some(c => t.includes(c));
    }

    /* ===== Lógica Abierto/Cerrado (en vivo) ===== */
    const RE_DIA = "(?:lunes|martes|mi[\\u00e9e]rcoles|jueves|viernes|s[\\u00e1a]bados?|domingos?)";
    const RE_CONN = "(?:\\s*,\\s*|\\s+y\\s+|\\s+a\\s+)";
    const RE_DAYGROUP = "(?:los\\s+|las\\s+)?" + RE_DIA + "(?:" + RE_CONN + "(?:los\\s+|las\\s+)?" + RE_DIA + ")*";
    const RE_TIME = "(\\d{1,2})[:.](\\d{2})\\s+a\\s+(\\d{1,2})[:.](\\d{2})";

    function indiceDia(t) {
        t = t.toLowerCase();
        if (t.startsWith("lun")) return 0; if (t.startsWith("mar")) return 1;
        if (t.startsWith("mi")) return 2;  if (t.startsWith("jue")) return 3;
        if (t.startsWith("vie")) return 4; if (t.startsWith("s")) return 5;
        if (t.startsWith("dom")) return 6; return null;
    }
    function diasDeFrase(frase) {
        frase = frase.toLowerCase();
        const tokens = frase.match(new RegExp(RE_DIA, "g")) || [];
        const idx = tokens.map(indiceDia).filter(x => x !== null);
        if (!idx.length) return new Set();
        if (/\s+a\s+/.test(frase) && idx.length >= 2) {
            let ini = idx[0], fin = idx[idx.length - 1], s = new Set();
            if (ini <= fin) for (let d = ini; d <= fin; d++) s.add(d);
            else { for (let d = ini; d <= 6; d++) s.add(d); for (let d = 0; d <= fin; d++) s.add(d); }
            return s;
        }
        return new Set(idx);
    }
    function parsearHorario(h) {
        if (!h) return [];
        const s = h.toLowerCase();
        if (/24\s*h/.test(s)) return "SIEMPRE";
        const ev = []; let m;
        const rd = new RegExp(RE_DAYGROUP, "g");
        while ((m = rd.exec(s)) !== null) { if (m[0].trim() !== "") ev.push([m.index, "dias", m[0]]); if (m.index === rd.lastIndex) rd.lastIndex++; }
        const rt = new RegExp(RE_TIME, "g");
        while ((m = rt.exec(s)) !== null) ev.push([m.index, "rango", [parseInt(m[1])*60+parseInt(m[2]), parseInt(m[3])*60+parseInt(m[4])]]);
        ev.sort((a, b) => a[0] - b[0]);
        const bloques = []; let dias = new Set();
        for (const [, tipo, val] of ev) { if (tipo === "dias") dias = diasDeFrase(val); else if (dias.size) bloques.push([dias, val]); }
        return bloques;
    }
    function estadoPunto(h, ahora) {
        ahora = ahora || new Date();
        const b = parsearHorario(h);
        if (b === "SIEMPRE") return ["Abierto", "abierto"];
        if (!b.length) return ["Horario no disponible", "desconocido"];
        const dia = (ahora.getDay() + 6) % 7, min = ahora.getHours()*60 + ahora.getMinutes();
        for (const [dias, [ini, fin]] of b) if (dias.has(dia) && ini <= min && min < fin) return ["Abierto", "abierto"];
        return ["Cerrado", "cerrado"];
    }

    /* ===== Mapa ===== */
    const map = L.map('map', { zoomControl: false }).setView([-45.5712, -72.0685], 13.5);
    L.control.zoom({ position: 'bottomright' }).addTo(map);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', { maxZoom: 19 }).addTo(map);

    const markers = [];
    PUNTOS.forEach((p, i) => {
        const hex = colorMap[p.color] || "#757575";
        const fa = iconMap[p.icono] || "fa-solid fa-recycle";
        const icon = L.divIcon({
            className: 'div-icon-eco',
            html: `<div class="pin-wrap" style="position:relative">
                     <div class="custom-marker-pin" style="background:${hex}"><i class="${fa}"></i></div>
                     <span class="estado-dot" data-dot="${i}"></span>
                   </div>`,
            iconSize: [34, 34], iconAnchor: [17, 34], popupAnchor: [0, -32]
        });
        const mk = L.marker([p.lat, p.lng], { icon }).addTo(map);
        mk.bindTooltip(p.nombre, { direction: 'top', offset: [0, -30] });
        mk.on('click', () => abrirDrawer(i));
        markers.push(mk);
    });

    /* ===== Filtros por categoría ===== */
    const visibles = {}; CATS.forEach(c => visibles[c.tipo] = true);
    function construirFiltros() {
        const cont = document.getElementById('filtros'); cont.innerHTML = '';
        CATS.forEach(c => {
            const total = PUNTOS.filter(p => p.tipo === c.tipo).length;
            const chip = document.createElement('div');
            chip.className = 'chip' + (visibles[c.tipo] ? '' : ' off');
            chip.innerHTML = `<span class="punto" style="background:${c.color}"><i class="${c.icono}"></i></span>
                              <span class="nom">${c.tipo}</span>
                              <span class="cnt">${total}</span>
                              <span class="check"><i class="fa-solid ${visibles[c.tipo] ? 'fa-eye' : 'fa-eye-slash'}"></i></span>`;
            chip.onclick = () => { visibles[c.tipo] = !visibles[c.tipo]; aplicarFiltros(); construirFiltros(); };
            cont.appendChild(chip);
        });
    }
    function aplicarFiltros() {
        PUNTOS.forEach((p, i) => {
            // Un punto se muestra si su tipo está visible Y (no hay material
            // seleccionado O el punto recibe ese material)
            const mostrar = visibles[p.tipo] && (!materialActivo || tieneMaterial(p, materialActivo));
            if (mostrar) { if (!map.hasLayer(markers[i])) markers[i].addTo(map); }
            else if (map.hasLayer(markers[i])) map.removeLayer(markers[i]);
        });
        actualizar(); // repinta los indicadores Abierto/Cerrado en los pines recién agregados
    }

    /* ===== Panel derecho: Categorías de materiales ===== */
    function construirMateriales() {
        const cont = document.getElementById('materiales'); cont.innerHTML = '';
        MATERIALES.forEach(m => {
            const total = PUNTOS.filter(p => tieneMaterial(p, m)).length;
            if (total === 0) return; // no mostrar categorías sin puntos asociados
            const chip = document.createElement('div');
            chip.className = 'mat-chip' + (materialActivo && materialActivo.id === m.id ? ' activo' : '');
            chip.innerHTML = `<span class="mi"><i class="${m.icono}"></i></span>
                              <span class="mn">${m.nombre}</span>
                              <span class="mc">${total}</span>`;
            chip.onclick = () => {
                // Clic en el material activo lo desactiva; en otro, lo selecciona
                materialActivo = (materialActivo && materialActivo.id === m.id) ? null : m;
                aplicarFiltros();
                construirMateriales();
            };
            cont.appendChild(chip);
        });
        document.getElementById('btn-limpiar-mat').classList.toggle('visible', !!materialActivo);
    }
    function limpiarMaterial() {
        materialActivo = null;
        aplicarFiltros();
        construirMateriales();
    }

    /* ===== Drawer de detalle ===== */
    function abrirDrawer(i) {
        const p = PUNTOS[i];
        const [et, cl] = estadoPunto(p.horario);
        const hex = colorMap[p.color] || "#0E5680";
        document.getElementById('drawer-head').style.background = `linear-gradient(135deg, ${hex}, ${sombra(hex)})`;
        document.getElementById('d-tipo').textContent = p.tipo || '';
        document.getElementById('d-nombre').textContent = p.nombre || 'Sin nombre';
        const badge = document.getElementById('d-estado');
        badge.textContent = et; badge.className = 'badge b-' + cl;
        badge.style.background = 'rgba(255,255,255,0.92)';
        badge.style.color = cl === 'abierto' ? '#1b7a32' : (cl === 'cerrado' ? '#c62828' : '#5d6b76');
        badge.style.border = 'none';
        document.getElementById('d-desc').textContent = p.descripcion || 'Sin información de dirección.';
        document.getElementById('d-horario').textContent = p.horario || 'Sin horario especificado.';
        document.getElementById('d-si').textContent = p.detalle || p.residuos || 'No hay detalles específicos.';
        document.getElementById('d-no').textContent = p.no_reciclar || 'Sin restricciones listadas.';
        document.getElementById('d-ruta').href = `https://www.google.com/maps/dir/?api=1&destination=${p.lat},${p.lng}`;
        document.getElementById('overlay').classList.add('open');
        document.getElementById('drawer').classList.add('open');
        map.panTo([p.lat, p.lng], { animate: true });
    }
    function cerrarDrawer() {
        document.getElementById('overlay').classList.remove('open');
        document.getElementById('drawer').classList.remove('open');
    }
    function sombra(hex) {
        const n = parseInt(hex.slice(1), 16);
        let r = (n >> 16) - 35, g = ((n >> 8) & 255) - 35, b = (n & 255) - 35;
        r = Math.max(0, r); g = Math.max(0, g); b = Math.max(0, b);
        return '#' + (r << 16 | g << 8 | b).toString(16).padStart(6, '0');
    }
    document.addEventListener('keydown', e => { if (e.key === 'Escape') cerrarDrawer(); });

    /* ===== Estado en vivo: KPIs, reloj y marcadores ===== */
    const meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
    const dias = ['domingo','lunes','martes','miércoles','jueves','viernes','sábado'];
    function actualizar() {
        const ahora = new Date();
        let abiertos = 0;
        PUNTOS.forEach((p, i) => {
            const [, cl] = estadoPunto(p.horario, ahora);
            if (cl === 'abierto') abiertos++;
            const dot = document.querySelector(`[data-dot="${i}"]`);
            const pin = markers[i].getElement() ? markers[i].getElement().querySelector('.custom-marker-pin') : null;
            if (dot) dot.style.background = cl === 'abierto' ? '#43a047' : (cl === 'cerrado' ? '#e53935' : '#9e9e9e');
            if (pin) pin.classList.toggle('marker-cerrado', cl === 'cerrado');
        });
        const total = PUNTOS.length;
        document.getElementById('kpi-abiertos').textContent = abiertos;
        document.getElementById('kpi-total').textContent = total;
        document.getElementById('s-total').textContent = total;
        document.getElementById('s-abiertos').textContent = abiertos;
        document.getElementById('s-cerrados').textContent = total - abiertos;
        document.getElementById('reloj-hora').textContent =
            String(ahora.getHours()).padStart(2, '0') + ':' + String(ahora.getMinutes()).padStart(2, '0');
        document.getElementById('reloj-fecha').textContent =
            dias[ahora.getDay()] + ', ' + ahora.getDate() + ' de ' + meses[ahora.getMonth()];
    }

    construirFiltros();
    construirMateriales();
    actualizar();
    setInterval(actualizar, 20000); // refresco en vivo cada 20 s
</script>
</body>
</html>
"""

# ========================================================
# 3. SERVIDOR FLASK
# ========================================================
# Flask sirve automáticamente la carpeta "static/" en la ruta "/static"
app = Flask(__name__, static_folder="static", static_url_path="/static")

# Carpeta donde el notebook de instalación deja las librerías descargadas
VENDOR_DIR = os.path.join("static", "vendor")


def _existe_vendor(ruta_relativa):
    """True si el archivo local de una librería ya fue descargado."""
    return os.path.exists(os.path.join(VENDOR_DIR, ruta_relativa))


def construir_head_assets():
    """Arma las etiquetas del <head>: usa las librerías LOCALES si existen
    (modo recomendado para redes con bloqueos); si no, usa el CDN de internet."""
    lineas = []

    # Hoja de estilos de Leaflet
    if _existe_vendor("leaflet/leaflet.css"):
        lineas.append('<link rel="stylesheet" href="/static/vendor/leaflet/leaflet.css" />')
    else:
        lineas.append('<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />')

    # Tipografías (Baloo 2 + Montserrat)
    if _existe_vendor("fonts/fonts.css"):
        lineas.append('<link rel="stylesheet" href="/static/vendor/fonts/fonts.css" />')
    else:
        lineas.append('<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">')

    # Iconos Font Awesome
    if _existe_vendor("fontawesome/css/all.min.css"):
        lineas.append('<link rel="stylesheet" href="/static/vendor/fontawesome/css/all.min.css" />')
    else:
        lineas.append('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />')

    # Script de Leaflet
    if _existe_vendor("leaflet/leaflet.js"):
        lineas.append('<script src="/static/vendor/leaflet/leaflet.js"></script>')
    else:
        lineas.append('<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>')

    return "\n    ".join(lineas)


@app.route("/")
def dashboard():
    puntos = cargar_puntos()
    html = HTML_DASHBOARD.replace("__PUNTOS_JSON__", json.dumps(puntos, ensure_ascii=False))
    html = html.replace("__ASSETS_HEAD__", construir_head_assets())
    return Response(html, mimetype="text/html")


def abrir_navegador():
    webbrowser.open("http://127.0.0.1:5000")


# ========================================================
# Punto de entrada
# - En un servidor (Render, etc.) se ejecuta con: gunicorn app:app
#   (gunicorn importa el objeto "app" y NO corre este bloque).
# - En tu PC puedes ejecutarlo con: python app.py
# ========================================================
if __name__ == "__main__":
    # Usa el puerto que asigna la plataforma de hosting (PORT) o 5000 en local
    port = int(os.environ.get("PORT", "5000"))
    en_local = os.environ.get("PORT") is None

    if en_local:
        print("=" * 52)
        print("  EcoRuta · Dashboard de Reciclaje de Coyhaique")
        print(f"  Abriendo en el navegador: http://127.0.0.1:{port}")
        print("  (para cerrar el servidor, presiona CTRL+C)")
        print("=" * 52)
        # Solo en local abrimos el navegador automáticamente
        threading.Timer(1.0, abrir_navegador).start()

    # host="0.0.0.0" permite que el servidor acepte visitas desde internet
    app.run(host="0.0.0.0", port=port, debug=False)

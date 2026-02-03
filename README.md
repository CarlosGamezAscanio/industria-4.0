# Sistema de Monitoreo Industrial 4.0

Sistema de monitoreo industrial con interfaz gráfica que simula sensores de temperatura y presión, incluye autenticación de usuarios y almacenamiento de datos históricos con visualización avanzada.

## Características

- 🔐 **Autenticación segura** con base de datos SQLite
- 📊 **Simulación en tiempo real** de sensores industriales
- ⚠️ **Sistema de alertas** automáticas para valores críticos
- 💾 **Almacenamiento automático** de todas las lecturas
- 📋 **Historial completo** con tabla detallada y estadísticas
- 📈 **Gráficas interactivas** con análisis temporal avanzado
- 🎨 **Interfaz** con tema oscuro y colores intuitivos

## Requisitos

- Python 3.7 o superior
- Windows (los scripts están optimizados para Windows)

## Instalación y Ejecución

### Método Automático (Recomendado)

**PowerShell:**
```powershell
.\run.ps1
```

**CMD:**
```cmd
run.bat
```

### Método Manual

1. **Crear entorno virtual:**
```cmd
python -m venv .venv
```

2. **Activar entorno virtual:**
```cmd
.venv\Scripts\activate.bat
```

3. **Instalar dependencias:**
```cmd
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**
```cmd
python main.py
```

## Uso del Sistema

### 1. Inicio de Sesión
- **Usuario:** `admin`
- **Contraseña:** `1234`
- Presiona Enter para acceder rápidamente

### 2. Panel de Control
- **Monitoreo en tiempo real** de temperatura y presión
- **Alertas automáticas** cuando los valores superan los límites:
  - Temperatura > 90°C
  - Presión > 40 PSI
- **Guardado automático** cada 2 segundos en base de datos

### 3. Funciones Avanzadas
- **📊 Ver Registro:** Tabla completa con historial, estadísticas y filtros por estado
- **📈 Ver Gráfica:** Visualización temporal interactiva con:
  - Selector de cantidad de registros (10, 20, 50, 100, TODOS)
  - Líneas de umbral crítico y promedio
  - Área de alerta sombreada
  - Estadísticas en tiempo real

## Arquitectura del Sistema

```
├── main.py                 # 🚀 Punto de entrada principal
├── gui_login.py           # 🔐 Interfaz de autenticación
├── gui_dashboard.py       # 📊 Panel principal de monitoreo
├── ventanas_analisis.py   # 📈 Ventanas de registro y gráficas
├── auth.py               # 🛡️ Gestión de usuarios
├── database.py           # 💾 Manejo de SQLite
├── simulator.py          # 🔧 Simulador de sensores
├── requirements.txt      # 📦 Dependencias
├── run.ps1              # ⚡ Script PowerShell
├── run.bat              # ⚡ Script CMD
└── sistema_monitoreo.db # 🗄️ Base de datos (auto-creada)
```

## Especificaciones Técnicas

### Rangos de Sensores
- **Temperatura:** 20°C - 100°C (Alerta > 90°C)
- **Presión:** 1 PSI - 15 PSI (Alerta > 40 PSI)

### Base de Datos
- **Motor:** SQLite (archivo local)
- **Tablas:** usuarios, historial
- **Campos:** id, fecha, temperatura, presión, estado

### Tecnologías
- **GUI:** CustomTkinter (tema oscuro)
- **Gráficas:** Matplotlib con backend TkAgg
- **Base de datos:** SQLite3
- **Simulación:** Random con rangos realistas

## Solución de Problemas

### Errores Comunes

1. **Python no encontrado:**
   ```cmd
   python --version
   ```

2. **Problemas de dependencias:**
   ```cmd
   pip install --upgrade -r requirements.txt
   ```

3. **Error de matplotlib:**
   ```cmd
   pip install --upgrade matplotlib
   ```

4. **Base de datos bloqueada:**
   - Cierra todas las instancias de la aplicación
   - Reinicia y vuelve a ejecutar

### Rendimiento
- **Actualización:** Cada 2 segundos
- **Capacidad:** Ilimitados registros históricos
- **Memoria:** Optimizada para uso continuo
- **Gráficas:** Renderizado eficiente hasta 1000+ puntos

## Desarrollo y Mantenimiento

### Estructura del Código
- **Comentarios completos** en español
- **Funciones modulares** y reutilizables
- **Separación de responsabilidades** clara
- **Módulos independientes** para análisis y visualización
- **Manejo de errores** robusto

### Extensibilidad
- Fácil agregar nuevos tipos de sensores
- Sistema de alertas configurable
- Exportación de datos implementable
- Integración con APIs externas posible
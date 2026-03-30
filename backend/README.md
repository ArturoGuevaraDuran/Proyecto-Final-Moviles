# Control de Comedor Universitario - Backend API

API REST construida con Django y Django REST Framework para el sistema de control de asistencia y distribución de comida en el comedor universitario.

## Requisitos Previos

* Python 3.10+
* PostgreSQL (vía Docker o conexión a Supabase)
* Pipenv o Virtualenv (Recomendado)

## Configuración del Entorno de Desarrollo

1. **Clonar el repositorio y entrar a la carpeta backend:**
   ```bash
   cd backend

2. Crear y activar el entorno virtual:
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En Mac/Linux:
    source venv/bin/activate

3. Instalar dependencias
    pip install -r requirements.txt

4. Configurar variables de entorno
    # Copia el archivo .env.example y renómbralo a .env. con las credenciales correspondientes

### ⚠️ Nota importante sobre Supabase (Base de Datos)
    Debido a restricciones de red (IPv4 vs IPv6), **NO** utilices la conexión directa estándar de Supabase. 
    En tu archivo `.env`, debes utilizar la URL del **Session Pooler** que te da Supabase en su panel.
    * El dominio debe verse similar a: `aws-0-us-east-1.pooler.supabase.com`
    * Utiliza las credenciales del usuario `comedor_app`, **nunca** el usuario `postgres` por motivos de seguridad.

5. Aplicar migraciones de la base de datos:
    python manage.py migrate

6. Crear superusuario (Administrador):
    python manage.py createsuperuser

7. Ejecutar el servidor local:
    python manage.py runserver

## ⚠️ Notas Críticas sobre Base de Datos y Supabase

Si necesitas configurar el entorno desde cero o cambiar variables, ten en cuenta las siguientes reglas establecidas en nuestra arquitectura:

1. **Estructura de la Contraseña:** La contraseña del usuario de la base de datos **no debe contener** los caracteres `@` o `#`. Al usar URLs de conexión (ej. `postgres://user:pass@host`), el framework puede confundir estos símbolos con delimitadores de la URL, provocando fallos de autenticación.
2. **Conexión IPv4 y Pooler:** Supabase bloquea las conexiones IPv4 directas en planes gratuitos. Siempre debes conectarte usando el host del **Pooler** (ej. `aws-1-us-east-1.pooler.supabase.com`).
3. **Modo Session vs Transaction:** * Django requiere conexiones persistentes para hacer migraciones de forma segura. 
   * Asegúrate de que tu `DATABASE_URL` apunte al puerto **`5432`** (que en el Pooler de Supabase equivale al modo *Session*). Si usas el puerto `6543` (modo *Transaction*), Django arrojará el error `server didn't return client encoding`.
4. **Bloqueos de IP (Circuit Breaker):** Si intentas conectarte repetidamente con credenciales incorrectas, el sistema de seguridad de Supabase abrirá el "Circuit breaker" y bloqueará tu IP temporalmente. Si esto ocurre, un administrador debe entrar al panel de Supabase y remover el baneo en la sección *Network Bans*.
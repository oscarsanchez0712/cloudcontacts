# ☁️ CloudContacts - Agenda de Contactos en la Nube

Aplicación web desarrollada con Python, Flask y Tailwind CSS, desplegada en AWS EC2 con arquitectura de dos servidores.

## 🏗️ Arquitectura
- **EC2-WEB**: Servidor web público expuesto en el puerto 80. Corre Flask con Gunicorn detrás de Nginx.
- **EC2-DB**: Servidor de base de datos privado, solo accesible desde EC2-WEB por el puerto 3306.

## 🔐 Configuración de Grupos de Seguridad

### EC2-WEB
| Puerto | Protocolo | Origen |
|--------|-----------|--------|
| 22 | SSH | Mi IP |
| 80 | HTTP | 0.0.0.0/0 |

### EC2-DB
| Puerto | Protocolo | Origen |
|--------|-----------|--------|
| 22 | SSH | Mi IP |
| 3306 | MySQL | Security Group de EC2-WEB |

## 🗄️ Instalación de MySQL en EC2-DB

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install mysql-server -y
sudo systemctl start mysql
sudo systemctl enable mysql
sudo mysql
```

```sql
CREATE DATABASE cloudcontacts;
CREATE USER 'clouduser'@'%' IDENTIFIED BY 'cloudpass';
GRANT ALL PRIVILEGES ON cloudcontacts.* TO 'clouduser'@'%';
FLUSH PRIVILEGES;
USE cloudcontacts;
CREATE TABLE contactos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);
EXIT;
```

```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
# Cambiar: bind-address = 0.0.0.0
sudo systemctl restart mysql
```

## 🚀 Instalación en EC2-WEB

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv nginx -y
git clone https://github.com/oscarsanchez0712/cloudcontacts.git
cd cloudcontacts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configurar variables de entorno
```bash
nano .env
```
DB_HOST=<IP_PRIVADA_EC2_DB>

DB_USER=clouduser

DB_PASSWORD=cloudpass

DB_NAME=cloudcontacts
### Iniciar con Systemd
```bash
sudo systemctl start cloudcontacts
sudo systemctl enable cloudcontacts
sudo systemctl restart nginx
```

## 🌐 Acceso a la Aplicación

- **Formulario:** http://3.228.105.230
- **Lista de contactos:** http://3.228.105.230/contacts

## 👨‍💻 Autor

Diana Huamani - I.E.S.T.P. Valle Grande

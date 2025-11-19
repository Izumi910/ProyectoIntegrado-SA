#!/usr/bin/env python3
"""
Script para configurar Amazon SES para el proyecto Lilis Dulcería
"""

import boto3
import os
from botocore.exceptions import ClientError

def setup_ses():
    """Configurar Amazon SES"""
    
    # Obtener credenciales de AWS (deben estar configuradas en AWS Academy)
    try:
        ses_client = boto3.client('ses', region_name='us-east-1')
        
        # Verificar dominio o email
        email_to_verify = input("Ingresa el email que quieres verificar para enviar correos: ")
        
        try:
            response = ses_client.verify_email_identity(EmailAddress=email_to_verify)
            print(f"✅ Email {email_to_verify} enviado para verificación.")
            print("📧 Revisa tu bandeja de entrada y haz clic en el enlace de verificación.")
        except ClientError as e:
            print(f"❌ Error al verificar email: {e}")
            
        # Listar emails verificados
        try:
            response = ses_client.list_verified_email_addresses()
            verified_emails = response['VerifiedEmailAddresses']
            
            if verified_emails:
                print("\n📋 Emails verificados:")
                for email in verified_emails:
                    print(f"  - {email}")
            else:
                print("\n⚠️  No hay emails verificados aún.")
                
        except ClientError as e:
            print(f"❌ Error al listar emails verificados: {e}")
            
        # Verificar límites de envío
        try:
            response = ses_client.get_send_quota()
            print(f"\n📊 Límites de envío:")
            print(f"  - Máximo por 24h: {response['Max24HourSend']}")
            print(f"  - Máximo por segundo: {response['MaxSendRate']}")
            print(f"  - Enviados en 24h: {response['SentLast24Hours']}")
        except ClientError as e:
            print(f"❌ Error al obtener límites: {e}")
            
    except Exception as e:
        print(f"❌ Error de configuración: {e}")
        print("\n💡 Asegúrate de que:")
        print("  1. Estás en AWS Academy")
        print("  2. Tienes las credenciales AWS configuradas")
        print("  3. SES está disponible en tu región")

if __name__ == "__main__":
    print("🚀 Configurando Amazon SES para Lilis Dulcería...")
    setup_ses()
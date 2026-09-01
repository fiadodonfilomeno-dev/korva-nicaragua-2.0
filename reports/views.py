from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import AnalyticsReport
import csv
from datetime import datetime

@login_required(login_url='login')
def reports_view(request):
    """Vista de reportes del usuario"""
    profile = request.user.profile
    
    # Obtener o crear el reporte analítico
    report, created = AnalyticsReport.objects.get_or_create(user=profile)
    
    # Actualizar estadísticas
    report.total_posts = profile.posts.count()
    report.total_products = profile.products.count()
    report.total_collaborations = profile.collaborations_count
    report.save()
    
    context = {
        'profile': profile,
        'report': report,
    }
    
    return render(request, 'reports/reports.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def export_csv(request):
    """Exportar datos en formato CSV"""
    profile = request.user.profile
    
    # Crear respuesta CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="reporte_{profile.business_name}_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    # Escribir CSV
    writer = csv.writer(response)
    writer.writerow(['Reporte Analítico de Korva Nicaragua'])
    writer.writerow(['Empresa:', profile.business_name])
    writer.writerow(['RUC:', profile.ruc])
    writer.writerow(['Fecha:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow([])
    
    # Estadísticas principales
    writer.writerow(['ESTADÍSTICAS PRINCIPALES'])
    writer.writerow(['Métrica', 'Valor'])
    writer.writerow(['Puntuación de Popularidad', profile.popularity_score])
    writer.writerow(['Nivel/Tier', profile.tier_display])
    writer.writerow(['Seguidores', profile.followers_count])
    writer.writerow(['Aliados', profile.associates_count])
    writer.writerow(['Colaboraciones', profile.collaborations_count])
    writer.writerow(['Total de Posts', profile.posts.count()])
    writer.writerow(['Total de Productos', profile.products.count()])
    writer.writerow([])
    
    # Posts
    writer.writerow(['PUBLICACIONES RECIENTES'])
    writer.writerow(['Título', 'Contenido', 'Upvotes', 'Downvotes', 'Fecha'])
    for post in profile.posts.all()[:20]:
        writer.writerow([post.title, post.content[:50], post.upvotes, post.downvotes, post.timestamp])
    writer.writerow([])
    
    # Productos
    writer.writerow(['PRODUCTOS'])
    writer.writerow(['Nombre', 'Precio', 'Moneda', 'Categoría', 'Vistas'])
    for product in profile.products.all()[:20]:
        writer.writerow([product.name, product.price, product.currency, product.category, product.views_count])
    
    return response


@login_required(login_url='login')
@require_http_methods(["GET"])
def export_pdf(request):
    """Exportar datos en formato PDF"""
    profile = request.user.profile
    
    # Generar PDF usando reportlab
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
    from reportlab.lib import colors
    from io import BytesIO
    
    # Crear documento PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Crear estilo personalizado
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#10b981'),
        spaceAfter=30,
    )
    
    # Título
    elements.append(Paragraph(f"Reporte Analítico - {profile.business_name}", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Información básica
    info_data = [
        ['Empresa:', profile.business_name],
        ['RUC:', profile.ruc],
        ['Ciudad:', profile.get_city_display()],
        ['Sector:', profile.get_sector_display()],
        ['Nivel:', profile.tier_display],
        ['Fecha de Reporte:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Estadísticas
    elements.append(Paragraph("Estadísticas Principales", styles['Heading2']))
    elements.append(Spacer(1, 0.1*inch))
    
    stats_data = [
        ['Métrica', 'Valor'],
        ['Puntuación de Popularidad', str(profile.popularity_score)],
        ['Seguidores', str(profile.followers_count)],
        ['Aliados', str(profile.associates_count)],
        ['Colaboraciones', str(profile.collaborations_count)],
        ['Total de Publicaciones', str(profile.posts.count())],
        ['Total de Productos', str(profile.products.count())],
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(stats_table)
    
    # Construir PDF
    doc.build(elements)
    
    # Retornar PDF
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{profile.business_name}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    return response


import logging
import os
from pyrogram import Client, filters
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib import colors
from reportlab.lib.units import mm

async def generate_contact_pdf(
    data: list = [],
    header: list = [],
    filename: str = "my_pdf.pdf"
):
    # Combine header and contacts data correctly
    full_data = [header] + data

    # Estimate column widths dynamically based on content
    def get_col_widths(table_data):
        col_count = len(table_data[0])
        widths = [0] * col_count
        for row in table_data:
            for col_idx, cell in enumerate(row):
                text = str(cell)
                cell_width = stringWidth(text, "Helvetica", 10) + 12  # Add padding
                widths[col_idx] = max(widths[col_idx], cell_width)
        return widths

    col_widths = get_col_widths(full_data)
    total_table_width = sum(col_widths)

    # Calculate page width: table width + margins (20mm left + 20mm right)
    margin = 20 * mm
    page_width = total_table_width + 2 * margin
    page_height = A4[1]  # Use A4 height for consistency
    custom_page_size = (page_width, page_height)

    # Create PDF with dynamic page size
    pdf = SimpleDocTemplate(filename, pagesize=custom_page_size, leftMargin=margin, rightMargin=margin)
    elements = []

    # Create and style the table
    table = Table(full_data, colWidths=col_widths, repeatRows=1)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ])
    table.setStyle(style)

    elements.append(table)
    pdf.build(elements)

    return filename

@Client.on_message(filters.command('c2p') & filters.private & filters.user('self'))
async def contacts_to_pdf(client, message):
    await message.reply_text("**Generating PDF of your contacts...**", quote=True)
    try:
        contacts = await client.get_contacts()
        if not contacts:
            return await message.reply_text("**No contacts found to convert to PDF.**", quote=True)

        # Prepare header for the PDF table
        header = ["Count", "Name", "Phone Number", "Username", "DC Id", "Unique Id"]
        contact_info = []
        for count, user in enumerate(contacts, 1):
            contact_info.append([
                count,
                user.first_name or "N/A",
                user.phone_number or "N/A",
                user.username or "N/A",
                user.dc_id or "N/A",
                user.id or "N/A",
            ])

        pdf = await generate_contact_pdf(data=contact_info, header=header, filename="contacts_table.pdf")

        await message.reply_document(
            document=pdf,
            caption="Here is the PDF containing your contacts.",
            quote=True
        )
        os.remove(pdf)
    except Exception as e:
        logging.error(f"Error generating PDF: {e}")
        await message.reply_text(f"**An error occurred while generating the PDF:**\n{str(e)}", quote=True)


@Client.on_message(filters.command('start') & filters.user('self'))
async def start(client, message):
    await message.reply_text('hai i am alive')

@Client.on_message(filters.command('c_count') & filters.private & filters.user('self'))
async def contacts_count(client, message):
    c = await client.get_contacts_count()
    await message.reply_text(f"**Total Contacts: {c}** \n\nTo convert your contacts to PDF, please use the command in a private chat with me: `/c2p`.")


@Client.on_message(filters.command('rmc') & filters.private & filters.user('self'))                       
async def remove_none_ph_contacts(client, message):
    await message.reply_text("**Removing contacts without phone numbers...**", quote=True)
    try:
        contacts = await client.get_contacts()
        if not contacts:
            return await message.reply_text("**No contacts found to convert to PDF.**", quote=True)

        for user in contacts:
            if not user.phone_number:
                await client.delete_contacts(user.id)
        await message.reply_text("**Contacts without phone numbers have been removed.**", quote=True)

    except Exception as e:  
        logging.error(f"Error generating PDF: {e}")
        await message.reply_text(f"**An error occurred while generating the PDF:**\n{str(e)}", quote=True)


@Client.on_message(filters.command('g2p'))                       
async def chat_user_to_pdf(client, message):
    try:
        chat = message.chat

        contact_info = []
        table_headers = ["Count", "Name", "Phone", "Joined Date", "Username", "DC Id", "Unique Id"]

        count = 0
        async for member in client.get_chat_members(chat.id):
            count += 1
            user = member.user
            contact_info.append([
                count,
                user.first_name or "N/A", 
                user.phone_number or "N/A",
                member.joined_date.strftime('%Y-%m-%d %I:%M:%S %p') if member.joined_date else "N/A",
                user.username or "N/A", 
                user.dc_id or "N/A", 
                user.id or "N/A", 
            ])

        pdf = await generate_contact_pdf(data=contact_info, header=table_headers, filename="group_table.pdf")

        await client.send_document(
            'me',
            document=pdf,   
            caption=f"Here is the PDF containing your chat {chat.title}.",
        )
        os.remove(pdf)
    except Exception as e:  
        logging.error(f"Error generating PDF: {e}")
        await message.reply_text(f"**An error occurred while generating the PDF:**\n{str(e)}", quote=True)
        

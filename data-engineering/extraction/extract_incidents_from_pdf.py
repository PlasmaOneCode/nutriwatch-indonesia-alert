#!/usr/bin/env python3
"""
Script untuk ekstrak data insiden keracunan MBG dari PDF Wikipedia
dan merge dengan incident_records_starter.csv

Wilayah II (Jawa):
- DKI Jakarta
- Jawa Barat
- Jawa Tengah
- DI Yogyakarta (Daerah Istimewa Yogyakarta)
- Jawa Timur
- Banten
"""

import pandas as pd
import re
from datetime import datetime
from typing import List, Dict

# Define Wilayah II provinces
WILAYAH_II_PROVINCES = {
    'DKI Jakarta': 'DKI Jakarta',
    'Jakarta': 'DKI Jakarta',
    'Jawa Barat': 'Jawa Barat',
    'Jawa Tengah': 'Jawa Tengah',
    'DI Yogyakarta': 'DI Yogyakarta',
    'Daerah Istimewa Yogyakarta': 'DI Yogyakarta',
    'Yogyakarta': 'DI Yogyakarta',
    'Jawa Timur': 'Jawa Timur',
    'Banten': 'Banten'
}

# Incident data extracted manually from PDF Wikipedia
# Format: (date_str, province, regency/city, location_name, victim_count, notes)
INCIDENTS_FROM_PDF = [
    # Aceh (NOT Wilayah II - for reference)
    ("2025-09-29", "Nanggroe Aceh Darussalam", "Kabupaten Aceh Utara", "SDN 6 Matangkuli", 3, ""),
    ("2026-01-24", "Nanggroe Aceh Darussalam", "Kabupaten Aceh Timur", "TBA", 19, ""),
    ("2026-02-11", "Nanggroe Aceh Darussalam", "Kabupaten Aceh Singkil", "TK Bunga Al-Qur'an, Pesantren Modern Darul Mustafa", 33, ""),
    ("2026-02-26", "Nanggroe Aceh Darussalam", "Kabupaten Bireuen", "warga Simpang Mamplam dan Pandrah", 140, ""),
    ("2026-02-26", "Nanggroe Aceh Darussalam", "Kabupaten Aceh Selatan", "PAUD, SMA", 18, ""),
    
    # Sumatera Utara (NOT Wilayah II)
    ("2025-10-15", "Sumatera Utara", "Kabupaten Toba", "SD Tanding Laguboti, SMPN 1 Laguboti", 121, ""),
    ("2025-10-31", "Sumatera Utara", "Kabupaten Nias Utara", "SD 071027 Onozitoli Sawo", 26, ""),
    ("2026-02-09", "Sumatera Utara", "Kabupaten Dairi", "SMK Swasta HKBP Sidikalang, SMK Swasta Arina Sidikalang", 271, ""),
    ("2026-02-24", "Sumatera Utara", "Kabupaten Nias Selatan", "SDN 071123", 35, ""),
    ("2026-04-01", "Sumatera Utara", "Kabupaten Humbang Hasundutan", "SMPN 016 Nagasaribu, SMA Negeri 3 Lintongnihuta", 18, ""),
    ("2026-04-28", "Sumatera Utara", "Kabupaten Deli Serdang", "SD swasta terpadu As Syifa", 11, ""),
    
    # WILAYAH II STARTS HERE
    # DKI Jakarta
    ("2025-08-29", "DKI Jakarta", "Jakarta Selatan", "TBA", 3, ""),
    ("2025-09-08", "DKI Jakarta", "Jakarta Utara", "TBA, SMPN 277 Jakarta, Kelurahan Lagoa", 14, ""),
    ("2025-09-23", "DKI Jakarta", "Jakarta Selatan", "SMAN 15 Jakarta", 7, ""),
    ("2025-09-25", "DKI Jakarta", "Jakarta Timur", "SDN 07 Pulogebang", 6, ""),
    ("2025-09-30", "DKI Jakarta", "Jakarta Timur", "SDN 01 Gedong", 22, ""),
    ("2026-04-03", "DKI Jakarta", "Jakarta Timur", "SDN Pondok Kelapa 1, 7, 9, SMAN 91 Jakarta", 135, ""),
    ("2026-05-08", "DKI Jakarta", "Jakarta Timur", "SDN Cakung Timur 01, SDN Ujung Menteng 02, 03", 252, ""),
    ("2025-10-29", "DKI Jakarta", "Jakarta Barat", "SDN Meruya Selatan 01", 20, ""),
    ("2026-05-22", "DKI Jakarta", "Jakarta Barat", "SMPN 82 Jakarta", 116, ""),
    ("2026-04-01", "DKI Jakarta", "Jakarta Pusat", "SMPN 71 Jakarta Pusat", 48, ""),
    
    # Jawa Barat
    ("2025-01-14", "Jawa Barat", "Kabupaten Indramayu", "TBA", 6, ""),
    ("2025-08-22", "Jawa Barat", "Kabupaten Indramayu", "TBA", 2, ""),
    ("2025-04-21", "Jawa Barat", "Kabupaten Cianjur", "MAN 1 Cianjur, SMP PGRI Cianjur", 51, ""),
    ("2025-08-20", "Jawa Barat", "Kabupaten Cianjur", "Pondok Pesantren Darul Quran", 12, ""),
    ("2025-09-03", "Jawa Barat", "Kabupaten Cianjur", "MTs Islamiyah Sayang", 9, ""),
    ("2025-09-11", "Jawa Barat", "Kabupaten Cianjur", "SDN Salakawung, SMP Budi Luhur", 36, ""),
    ("2025-09-25", "Jawa Barat", "Kabupaten Cianjur", "SDN Taruna Bakti", 30, ""),
    ("2025-10-09", "Jawa Barat", "Kabupaten Cianjur", "Yayasan Raudhatul Muttaqin", 16, ""),
    ("2026-01-27", "Jawa Barat", "Kabupaten Cianjur", "SDN Wargasari", 300, ""),
    ("2026-04-17", "Jawa Barat", "Kabupaten Cianjur", "Desa Sukasirna, Desa Purabaya", 134, "Meninggal: 1 Orang"),
    ("2026-05-13", "Jawa Barat", "Kabupaten Cianjur", "SD Negeri Ciadeg", 19, ""),
    
    ("2025-04-29", "Jawa Barat", "Kota Bandung", "SMP Negeri 35 Bandung", 342, ""),
    ("2025-05-01", "Jawa Barat", "Kabupaten Tasikmalaya", "Beberapa Sekolah TK, SDN 1/2 Rajapolah, SMPN 1 Rajapolah", 400, ""),
    ("2025-09-18", "Jawa Barat", "Kabupaten Tasikmalaya", "SD Cikalong 1, PAUD di Cikalong", 52, ""),
    ("2025-10-02", "Jawa Barat", "Kabupaten Tasikmalaya", "SMK Negeri Cipatujah, SMP Negeri 4, Pondok Pesantren Nursyamsiah", 115, ""),
    ("2025-10-13", "Jawa Barat", "Kabupaten Tasikmalaya", "Posyandu Daerah Manonjaya", 11, "Balita: 11"),
    ("2025-10-17", "Jawa Barat", "Kabupaten Tasikmalaya", "SDN Margamulya", 13, ""),
    ("2026-04-08", "Jawa Barat", "Kabupaten Tasikmalaya", "SMAN 1 Cisayong", 119, ""),
    
    ("2025-05-07", "Jawa Barat", "Kota Bogor", "TK-SD-SMP-SMA Bosowa Bina Insani, SDN Kukupu 3, SDN Kedung Waringin, SDN Kedung Jaya 1-2, SMP Bina Greha", 223, ""),
    ("2025-11-14", "Jawa Barat", "Kota Bogor", "SDN 2/3 Batu Tulis, SD Lawang Gintung, SMK PUI", 50, ""),
    
    ("2025-07-31", "Jawa Barat", "Kabupaten Kuningan", "SMPN 1 Cilimus", 30, ""),
    ("2025-10-03", "Jawa Barat", "Kabupaten Kuningan", "SMP 1 Luragung, SMAN 1 Luragung", 200, ""),
    ("2025-11-28", "Jawa Barat", "Kabupaten Kuningan", "TBA", 74, ""),
    
    ("2025-08-06", "Jawa Barat", "Kabupaten Sukabumi", "SDN Puncak Batu, MI Cikadu, PAUD di Cipamingkis", 32, ""),
    ("2025-08-22", "Jawa Barat", "Kabupaten Sukabumi", "SDN 02 Parakansalak", 24, ""),
    ("2025-09-11", "Jawa Barat", "Kabupaten Sukabumi", "SMKN 1 Cibadak", 69, ""),
    ("2025-09-24", "Jawa Barat", "Kabupaten Sukabumi", "SMK Doa Bangsa", 32, ""),
    ("2026-01-28", "Jawa Barat", "Kabupaten Sukabumi", "PAUD Al Hadi, SDN Bojong Kopo, Gunung Biru, Loji, Sangrawayang, Cibutun, MA", 31, ""),
    ("2026-03-06", "Jawa Barat", "Kabupaten Sukabumi", "Ponpes Az-Zain", 47, ""),
    
    ("2025-08-14", "Jawa Barat", "Kabupaten Karawang", "TBA", 82, ""),
    ("2026-04-17", "Jawa Barat", "Kabupaten Karawang", "Balita, Ibu Menyusui", 46, ""),
    
    ("2025-08-21", "Jawa Barat", "Kabupaten Bandung", "SD Negeri Legok Hayam", 12, ""),
    ("2025-09-17", "Jawa Barat", "Kabupaten Garut", "SDN 2 Mandalasari, SMP Siti Aisyah, MA Siti Aisyah, MA Maarif Cilageni, SMA Siti Aisyah", 657, ""),
    ("2025-09-30", "Jawa Barat", "Kabupaten Garut", "SDN 3 Talagasari, SMPN 1 Kadungora, SMP PGRI Kadungora, SMA Annisa Kadungora", 307, ""),
    ("2026-05-21", "Jawa Barat", "Kabupaten Garut", "SD Negeri 2 Hegarsari", 57, ""),
    
    ("2025-09-22", "Jawa Barat", "Kabupaten Bandung Barat", "SD Negeri Cipari, MTs Darul Fiqri, SMK Pembangunan Bandung Barat", 1333, ""),
    ("2025-09-24", "Jawa Barat", "Kabupaten Bandung Barat", "TK Nurul Saadah, SMP Ciparai, SMK Karya Perjuangan, MTs Manarul Huda, SDN 1 Cihampelas, MTs Al Mukhtariyah, SMKN 1 Cihampelas, MA Al Mukhtariyah", 1333, ""),
    ("2025-10-14", "Jawa Barat", "Kabupaten Bandung Barat", "SMPN 1 Cisarua", 518, ""),
    ("2025-10-15", "Jawa Barat", "Kabupaten Bandung Barat", "SDN 1 Garuda, SD 1 Barukai, SMKN 1 Cisarua, SMP Karya Prestasi Mandiri, SMK Widya Karya, pesantren Bani Sulaiman", 518, ""),
    ("2025-10-23", "Jawa Barat", "Kabupaten Bandung Barat", "SMPN 1 Lembang", 30, ""),
    ("2025-10-28", "Jawa Barat", "Kabupaten Bandung Barat", "SDN 1/2 Cibodas, SDN 1 Sutenjaya, SDN Buahbatu, SMPN 4 Lembang, SMK Putra Nasional Cibodas", 236, ""),
    
    ("2025-11-11", "Jawa Barat", "Kabupaten Bandung Barat", "SMP Bina Karya", 21, ""),
    
    ("2025-09-25", "Jawa Barat", "Kabupaten Subang", "SD Rawalele", 11, ""),
    
    ("2025-09-25", "Jawa Barat", "Kabupaten Sumedang", "SMK Win Ujungjaya, SMK Rimba Bahari Situraja, SMA Negeri 1 Tomo", 164, ""),
    
    ("2025-09-26", "Jawa Barat", "Kabupaten Bogor", "SMPN 1 Jonggol", 4, ""),
    ("2025-10-01", "Jawa Barat", "Kabupaten Bogor", "SDN 02 Pasir Angin", 3, ""),
    ("2025-10-16", "Jawa Barat", "Kabupaten Bogor", "SDN Ciangsana 02 Bogor", 7, ""),
    ("2026-04-06", "Jawa Barat", "Kabupaten Bogor", "Warga Tanjung Sari", 107, ""),
    
    ("2025-09-29", "Jawa Barat", "Kabupaten Ciamis", "SMPN 4 Pamarican", 52, ""),
    ("2025-10-03", "Jawa Barat", "Kabupaten Ciamis", "SDN 1 Sindang Sari", 10, ""),
    
    ("2025-10-01", "Jawa Barat", "Kabupaten Pangandaran", "MI Attarbiyah Leuwiliang", 8, ""),
    
    ("2025-10-01", "Jawa Barat", "Kota Banjar", "SMPN 3 Banjar", 79, ""),
    
    ("2025-10-02", "Jawa Barat", "Kota Bekasi", "SDN Kota Baru 3 Bekasi", 6, ""),
    
    ("2025-10-22", "Jawa Barat", "Kota Cirebon", "SDN Kesenden", 13, ""),
    ("2025-11-04", "Jawa Barat", "Kabupaten Cirebon", "SDN 2 Setu Wetan", 20, ""),
    ("2026-03-10", "Jawa Barat", "Kabupaten Cirebon", "SMAN 1 Jamblang", 1, ""),
    
    ("2025-11-17", "Jawa Barat", "Kota Sukabumi", "MI Al Ihsan", 28, ""),
    
    ("2025-12-04", "Jawa Barat", "Kabupaten Majalengka", "TBA", 42, ""),
    ("2026-05-29", "Jawa Barat", "Kabupaten Majalengka", "SMP, SMA", 22, ""),
    
    ("2026-02-25", "Jawa Barat", "Kota Cimahi", "TK PGRI, TK Kartika, SDN Cimahi Mandiri 4, SDN Karangmekar 5, SMPN 6 Cimahi", 46, ""),
    
    # Jawa Tengah
    ("2025-01-16", "Jawa Tengah", "Kabupaten Sukoharjo", "SDN Dukuh 03 Sukoharjo", 50, "Insiden pertama sejak MBG dimulai 6 Januari 2025"),
    ("2025-04-14", "Jawa Tengah", "Kabupaten Batang", "SDN 5 Proyonanggan, TK Islam Al Karomah", 60, ""),
    ("2025-10-31", "Jawa Tengah", "Kabupaten Batang", "SMK Kandeman", 800, ""),
    
    ("2025-04-24", "Jawa Tengah", "Kabupaten Karanganyar", "SD Wonorejo", 2, "Plus 1 Kepala Sekolah"),
    ("2025-10-03", "Jawa Tengah", "Kabupaten Karanganyar", "TBA", 168, ""),
    ("2025-10-09", "Jawa Tengah", "Kabupaten Karanganyar", "TK Nglebak 1-2, SD Negeri 2 Nglebak, SDN 3 Ngeblak, SMP Negeri 1 Tawangmangu", 105, ""),
    ("2025-10-13", "Jawa Tengah", "Kabupaten Karanganyar", "SMPN 1 Colomadu", 17, ""),
    ("2025-10-15", "Jawa Tengah", "Kabupaten Karanganyar", "SMPN 1 Karanganyar", 300, "Ratusan siswa"),
    
    ("2025-08-11", "Jawa Tengah", "Kabupaten Sragen", "SD Negeri 3-4 Gemolong, SD Negeri Gemolong, SMP Negeri 1-2-3 Gemolong, TBA", 251, ""),
    
    ("2025-09-10", "Jawa Tengah", "Kabupaten Klaten", "Siswa SD", 105, ""),
    ("2025-10-08", "Jawa Tengah", "Kabupaten Klaten", "SMPN 1 Wedi", 49, ""),
    ("2026-04-08", "Jawa Tengah", "Kabupaten Klaten", "SMKN 1 Klaten", 10, ""),
    ("2026-04-10", "Jawa Tengah", "Kabupaten Klaten", "SMPN 1 Kalikotes", 81, ""),
    ("2026-04-28", "Jawa Tengah", "Kabupaten Klaten", "SMPN 1 Tulung", 584, "Plus Guru"),
    
    ("2025-09-11", "Jawa Tengah", "Kabupaten Wonogiri", "Madrasah Ibtidaiyah Negeri Wonogiri", 23, ""),
    ("2025-09-12", "Jawa Tengah", "Kabupaten Wonogiri", "SMAN 2 Wonogiri", 110, ""),
    ("2025-09-30", "Jawa Tengah", "Kabupaten Wonogiri", "Ponpes Baitul Quran, SMAN 1 Slogohimo", 131, ""),
    ("2026-01-12", "Jawa Tengah", "Kabupaten Wonogiri", "TBA", 206, ""),
    ("2026-05-06", "Jawa Tengah", "Kabupaten Wonogiri", "SMKN 1 Jatiroto", 235, "Plus 7 Guru"),
    
    ("2025-09-22", "Jawa Tengah", "Kota Salatiga", "MAN Kota Salatiga", 7, ""),
    ("2025-10-03", "Jawa Tengah", "Kota Salatiga", "SMP Negeri 8 Salatiga", 192, ""),
    ("2025-10-06", "Jawa Tengah", "Kota Salatiga", "TBA", 12, ""),
    
    ("2025-09-23", "Jawa Tengah", "Kabupaten Jepara", "TK Melati Banjaran, Kelompok Bermain Darul Karomah Srikandang, MI Matholiul Huda Srikandang, SDN 1 Banjaran", 35, ""),
    
    ("2025-09-24", "Jawa Tengah", "Kabupaten Rembang", "SMPN 1 Kragan", 173, ""),
    ("2026-04-21", "Jawa Tengah", "Kabupaten Rembang", "SDN Balongmulyo", 22, ""),
    
    ("2025-09-22", "Jawa Tengah", "Kabupaten Banyumas", "TK, SDN Kediri, SDN Pangebatan", 408, ""),
    ("2025-09-29", "Jawa Tengah", "Kabupaten Banyumas", "SD 1-2-3 Sudagaran", 94, ""),
    
    ("2025-09-25", "Jawa Tengah", "Kabupaten Kebumen", "SDN Tegalretno, Madrasah Wathoniyah Islamiyah", 176, ""),
    
    ("2025-09-30", "Jawa Tengah", "Kabupaten Semarang", "SDN 01 Ungaran", 20, ""),
    
    ("2025-09-30", "Jawa Tengah", "Kabupaten Temanggung", "SMAN 2-3 Temanggung", 414, ""),
    ("2026-05-18", "Jawa Tengah", "Kabupaten Temanggung", "SMP Negeri 4 Temanggung + 7 Sekolah Lainnya", 323, ""),
    
    ("2025-10-03", "Jawa Tengah", "Kabupaten Purworejo", "SMPN 8 Purworejo, SMAN 3 Purworejo", 134, ""),
    
    ("2025-11-18", "Jawa Tengah", "Kabupaten Magelang", "Pondok Pesatren Nurul Ali", 112, ""),
    
    ("2025-11-26", "Jawa Tengah", "Kabupaten Blora", "SMPN 1 Blora, SMP Katolik Blora, SMP Kristen Blora", 810, ""),
    
    ("2025-11-26", "Jawa Tengah", "Kabupaten Kendal", "SMPN 1 Kendal", 17, ""),
    
    ("2025-12-11", "Jawa Tengah", "Kabupaten Grobogan", "Desa Putatsari", 23, ""),
    ("2026-01-10", "Jawa Tengah", "Kabupaten Grobogan", "TK Ngroto, SDN Trisari, SDN Glapan, SDN Penadaran, SMP Miftahul Huda, SMK Miftahul Huda", 803, ""),
    ("2026-01-30", "Jawa Tengah", "Kabupaten Grobogan", "SDN 2 Pulongrambe, SDN 3 Mayahan", 8, ""),
    
    ("2026-01-08", "Jawa Tengah", "Kota Semarang", "SMKN 11 Semarang", 75, ""),
    
    ("2026-01-13", "Jawa Tengah", "Kabupaten Pekalongan", "SDN 01 Kedungwuni", 15, ""),
    
    ("2026-01-22", "Jawa Tengah", "Kota Magelang", "SMPN 10 Kota Magelang", 75, "Plus 5 Guru"),
    
    ("2026-01-29", "Jawa Tengah", "Kabupaten Kudus", "SMAN 2 Kudus", 600, ""),
    
    ("2026-02-06", "Jawa Tengah", "Kabupaten Wonosobo", "SD Negeri 1 Kapulogo", 26, ""),
    
    ("2026-02-09", "Jawa Tengah", "Kabupaten Pati", "SMKN 4 Pati", 22, ""),
    
    ("2026-02-23", "Jawa Tengah", "Kota Tegal", "SMP PIUS", 3, ""),
    
    ("2026-03-12", "Jawa Tengah", "Kabupaten Pemalang", "TK", 1, ""),
    
    ("2026-04-18", "Jawa Tengah", "Kabupaten Demak", "Ponpes Bustanul Qur'an, Ponpes Asnawiyah, Ponpes Hidayatul Mubdtadiin, Ponpes Al Ma'arif, Ponpes Nurul Sakinah, MI Yosua", 189, ""),
    
    ("2026-04-29", "Jawa Tengah", "Kabupaten Cilacap", "Ponpes putri Kelurahan Gumilir", 100, ""),
    
    # DI Yogyakarta
    ("2025-06-17", "DI Yogyakarta", "Kabupaten Kulon Progo", "TK Aisyiyah Bustanul Athfal (ABA) Kasatriyan", 10, ""),
    ("2025-07-31", "DI Yogyakarta", "Kabupaten Kulon Progo", "SMPN 2 Wates, SMP Muhammadiyah 2 Wates, SD Triharjo, SD Sogan", 497, ""),
    ("2026-01-20", "DI Yogyakarta", "Kabupaten Kulon Progo", "PAUD, TK, SD", 104, ""),
    
    ("2025-08-13", "DI Yogyakarta", "Kabupaten Sleman", "SMP Muhammadiyah 1/3 Mlati, SMP Negeri 3 Mlati, SMP Pamungkas Mlati", 379, ""),
    ("2025-08-27", "DI Yogyakarta", "Kabupaten Sleman", "SMPN 3 Berbah", 135, "Plus 2 Guru"),
    ("2025-10-24", "DI Yogyakarta", "Kabupaten Sleman", "SD Jombor Lor, SMP Negeri 2 Mlati, MAN 3 Yogyakarta", 300, ""),
    
    ("2025-09-03", "DI Yogyakarta", "Kabupaten Gunungkidul", "MTsN Wonosari", 5, ""),
    ("2025-09-15", "DI Yogyakarta", "Kabupaten Gunungkidul", "SDN Sumberejo, SMPN 2 Semin, SMPS Budi Mulia Semin", 19, ""),
    ("2025-10-03", "DI Yogyakarta", "Kabupaten Gunungkidul", "SD Negeri 03 Piyaman", 6, ""),
    ("2025-10-28", "DI Yogyakarta", "Kabupaten Gunungkidul", "SMPN 1 Saptosari, SMKN 1 Saptosari", 695, ""),
    ("2025-10-29", "DI Yogyakarta", "Kabupaten Gunungkidul", "SD Sumbergiri, SDN Mendak 1, SMPN 1 Ponjong, SMA Pembangunan 3 Ponjong, SMK Ma'Arif, SMK Muhammadiyah", 121, ""),
    ("2025-11-03", "DI Yogyakarta", "Kabupaten Gunungkidul", "TBA", 547, ""),
    ("2026-01-23", "DI Yogyakarta", "Kabupaten Gunungkidul", "SMP Muhammadiyah Playen", 48, "Plus 9 Guru, 1 Kepala Sekolah"),
    
    ("2025-10-15", "DI Yogyakarta", "Kota Yogyakarta", "SMAN 1 Yogyakarta, SMA Muhammadiyah 7 Yogyakarta", 426, ""),
    
    ("2025-10-31", "DI Yogyakarta", "Kabupaten Bantul", "SD 2 Bakulan, SMPN 1 Jetis, SMPN 3 Jetis, SMP Muhammadiyah Pulokasang, SMAN 1 Jetis", 237, ""),
    ("2026-04-02", "DI Yogyakarta", "Kabupaten Bantul", "6 SD", 156, ""),
    ("2026-04-08", "DI Yogyakarta", "Kabupaten Bantul", "SDN Monggang, SD Negeri Kategan", 19, ""),
    ("2026-04-13", "DI Yogyakarta", "Kabupaten Bantul", "SMPN 3 Jetis, SMP Muhammadiyah", 80, ""),
    ("2026-05-06", "DI Yogyakarta", "Kabupaten Bantul", "SDN Kowang", 23, ""),
    
    # Jawa Timur
    ("2024-10-02", "Jawa Timur", "Kabupaten Nganjuk", "SDN Banaran I", 7, ""),
    ("2026-04-07", "Jawa Timur", "Kabupaten Nganjuk", "SDN Mojokendil", 50, "Puluhan Siswa"),
    
    ("2025-09-04", "Jawa Timur", "Kabupaten Situbondo", "SMAN 1 Panji", 232, ""),
    
    ("2025-09-09", "Jawa Timur", "Kabupaten Pamekasan", "Lembaga Pendidikan Al-Falah, Lembaga Pendidikan Al-Amin", 37, ""),
    ("2025-09-17", "Jawa Timur", "Kabupaten Pamekasan", "SDN Pasanggar 1 Pegantenan", 8, ""),
    ("2025-10-15", "Jawa Timur", "Kabupaten Pamekasan", "SDN Toronan 1", 9, ""),
    ("2025-11-06", "Jawa Timur", "Kabupaten Pamekasan", "MTS Al-Ula, MA Al Islamiyah Blumbungan", 17, ""),
    
    ("2025-09-17", "Jawa Timur", "Kabupaten Lamongan", "SMAN 2 Lamongan", 18, ""),
    
    ("2025-09-24", "Jawa Timur", "Kabupaten Bojonegoro", "SDN Semanding", 7, ""),
    ("2025-10-01", "Jawa Timur", "Kabupaten Bojonegoro", "SMAN 1 Kedungadem", 544, ""),
    ("2025-10-02", "Jawa Timur", "Kabupaten Bojonegoro", "SD Negeri Tumbrasanom, MTs Plus Nabawi", 7, ""),
    ("2025-11-28", "Jawa Timur", "Kabupaten Bojonegoro", "Pondok Pesantren Al Falah", 30, ""),
    ("2026-04-15", "Jawa Timur", "Kabupaten Bojonegoro", "TK, SD, Ibu Hamil", 17, ""),
    
    ("2025-09-24", "Jawa Timur", "Kabupaten Tuban", "SMKN 1 Palang", 6, ""),
    ("2025-10-14", "Jawa Timur", "Kabupaten Tuban", "SMKN Tambakboyo", 8, ""),
    ("2026-01-27", "Jawa Timur", "Kabupaten Tuban", "SMPN 1 Montong", 14, ""),
    
    ("2025-09-25", "Jawa Timur", "Kota Batu", "SMPN 1 Kota Batu, SMAN 1 Kota Batu", 12, ""),
    
    ("2025-09-26", "Jawa Timur", "Kabupaten Jember", "SDN 05 Sidomekar", 16, ""),
    ("2026-02-05", "Jawa Timur", "Kabupaten Jember", "SMP Negeri 1 Umbulsari", 112, ""),
    ("2026-05-20", "Jawa Timur", "Kabupaten Jember", "PAUD Qur'an Raudlatul Tulab, TK Al-Hidayah 01, RA Hidayatul Mubtadiin, PAUD Aster 29, TK Kuncup Bunga", 25, ""),
    
    ("2025-10-01", "Jawa Timur", "Kabupaten Ngawi", "SMK Negeri 1 Sine, MTs Muhammadiyah Sine", 51, ""),
    ("2025-10-02", "Jawa Timur", "Kabupaten Ngawi", "Belum Selesai SMKN 1, 5 Siswi MTs", 5, ""),
    ("2025-11-26", "Jawa Timur", "Kabupaten Ngawi", "SDN 2-6 Jenggrik, SDN 5 Gemarang, SMPN 2 Kedunggalar, SMAN 1 Kedunggalar", 87, ""),
    ("2025-12-04", "Jawa Timur", "Kabupaten Ngawi", "Ponpes Absoru Sunah, Ponpes Miftahul Janah, SDN 2-3-5 Mantingan, SD", 220, ""),
    ("2026-02-13", "Jawa Timur", "Kabupaten Ngawi", "Ponpes Al hijrah", 67, ""),
    
    ("2025-10-13", "Jawa Timur", "Kabupaten Tulungagung", "SDN 1 Tanggung, SMPN 1 Boyolangu", 68, ""),
    ("2026-01-20", "Jawa Timur", "Kabupaten Tulungagung", "SMKN 3 Boyolangu", 123, ""),
    ("2026-01-22", "Jawa Timur", "Kabupaten Tulungagung", "SMK Sore Tulungagung", 15, ""),
    ("2026-02-10", "Jawa Timur", "Kabupaten Tulungagung", "SDN 3 Bungur", 24, ""),
    
    ("2025-10-17", "Jawa Timur", "Kabupaten Magetan", "SDN 2 Kediren, MI Nurul Dholam", 12, ""),
    
    ("2025-10-23", "Jawa Timur", "Kabupaten Banyuwangi", "MAN 1 Banyuwangi", 112, ""),
    ("2025-10-29", "Jawa Timur", "Kabupaten Banyuwangi", "SMPN 3 Kalipuro, MA Nurul Khairoh, SMA NU Gombengsari", 133, ""),
    
    ("2025-10-23", "Jawa Timur", "Kabupaten Malang", "MTs Al-Khalifah", 38, ""),
    ("2026-02-11", "Jawa Timur", "Kabupaten Malang", "MI Al Maarif 9", 9, ""),
    
    ("2025-11-27", "Jawa Timur", "Kabupaten Madiun", "SDN Klecorejo, SDN 1 Darmorejo, SDN 2 Kebonagung", 49, ""),
    
    ("2025-12-03", "Jawa Timur", "Kabupaten Bondowoso", "SDN 1-2 Sukorejo, SMP, SMA", 77, ""),
    
    ("2026-01-10", "Jawa Timur", "Kabupaten Mojokerto", "Ponpes An-Nur, Ponpes Al-Hidayah, SMPN 2 Kutorejo", 780, ""),
    ("2026-04-09", "Jawa Timur", "Kabupaten Mojokerto", "TK Kartika, SDN Randubango, MI Mi'rojul Ulum, SMK PGRI Mojosari, SMA PGRI Mojosari", 79, ""),
    
    ("2026-01-15", "Jawa Timur", "Kota Mojokerto", "SDN 5-6 Wates, SMAN 2 Mojokerto", 50, "TBA Spesifik"),
    
    ("2026-02-02", "Jawa Timur", "Kota Surabaya", "SDN 1 Babat Jerawat", 27, ""),
    ("2026-05-11", "Jawa Timur", "Kota Surabaya", "TK Ubaid, TK Aletheia, SD Tembok Dukuh 1,3,4, SD Aletheia, SD Pancasila 45, SD Raden Wijaya, SD Ubaid 1-2, SMP Aletheia, SMP Islam, RW X Demak Jaya (warga)", 210, ""),
    
    ("2026-02-05", "Jawa Timur", "Kabupaten Trenggalek", "SD, SMP", 157, ""),
    
    ("2026-03-05", "Jawa Timur", "Kabupaten Jombang", "Ponpes Sholawat Darut Taubah", 31, ""),
    
    ("2026-04-09", "Jawa Timur", "Kabupaten Pacitan", "TK, SD, SMP", 158, ""),
    
    ("2026-04-16", "Jawa Timur", "Kota Madiun", "SDN 1 Demangan", 18, ""),
    
    ("2026-04-20", "Jawa Timur", "Kabupaten Bangkalan", "SMPN 1 Blega", 2, "Plus 1 Guru"),
    ("2026-06-04", "Jawa Timur", "Kabupaten Bangkalan", "SMAN 1 Kokop", 84, ""),
    
    ("2026-04-22", "Jawa Timur", "Kota Kediri", "SDN Ketami 1-2, SDN Tempurejo 1", 73, ""),
    
    ("2026-04-22", "Jawa Timur", "Kabupaten Sampang", "SDN Bira Tengah 1", 19, ""),
    
    ("2026-04-27", "Jawa Timur", "Kabupaten Kediri", "TK, SD", 6, ""),
    
    ("2026-05-21", "Jawa Timur", "Kabupaten Gresik", "SDN 238 Menganti", 14, ""),
    
    # Banten
    ("2025-01-19", "Banten", "Kabupaten Pandeglang", "SDN 2 Alaswangi", 28, ""),
    ("2025-09-02", "Banten", "Kabupaten Serang", "SMPN 1 Kramatwatu", 27, ""),
    ("2025-09-15", "Banten", "Kota Tangerang Selatan", "SD", 50, "TBA"),
    ("2026-04-08", "Banten", "Kota Tangerang", "TK, SMK Farmasi, Pesantren WH Tahfidz", 100, ""),
    ("2026-04-16", "Banten", "Kota Cilegon", "MTs Al-Inayah", 49, ""),
    ("2026-04-20", "Banten", "Kota Cilegon", "SDN Cikerai 2", 19, ""),
    ("2026-04-22", "Banten", "Kota Cilegon", "SMP PGRI Citangkil", 11, ""),
    ("2026-04-29", "Banten", "Kabupaten Tangerang", "TBA", 33, ""),
    ("2026-05-24", "Banten", "Kabupaten Serang", "SMAN 1 Padarincang", 32, ""),
]

def parse_date(date_str: str) -> pd.Timestamp:
    """Parse date string in format DD-MM-YYYY or YYYY-MM-DD"""
    try:
        # Try YYYY-MM-DD first (ISO format)
        return pd.to_datetime(date_str, format='%Y-%m-%d')
    except:
        try:
            # Try DD-MM-YYYY
            return pd.to_datetime(date_str, format='%d-%m-%Y')
        except:
            return None

def create_incidents_dataframe() -> pd.DataFrame:
    """Create DataFrame from extracted incidents"""
    records = []
    
    for date_str, province, regency, location_name, victim_count, notes in INCIDENTS_FROM_PDF:
        date_obj = parse_date(date_str)
        if date_obj is None:
            continue
            
        region_mapped = WILAYAH_II_PROVINCES.get(province, province)
        
        records.append({
            'date': date_obj,
            'sppg_name': '',  # Not available in Wikipedia data
            'location': f"{regency} - {location_name}" if location_name else regency,
            'region': region_mapped,
            'victim_count': victim_count,
            'source': 'Wikipedia',
            'notes': notes
        })
    
    df = pd.DataFrame(records)
    return df

def load_starter_csv() -> pd.DataFrame:
    """Load incident_records_starter.csv"""
    try:
        df = pd.read_csv('incident_records_starter.csv')
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        return df
    except FileNotFoundError:
        print("incident_records_starter.csv not found")
        return pd.DataFrame()

def _normalize_location(loc: str) -> str:
    """Normalize location string for dedup matching."""
    import unicodedata
    s = str(loc).lower().strip()
    s = unicodedata.normalize('NFKD', s)
    # Remove common prefixes/suffixes that vary between sources
    for prefix in ['kabupaten ', 'kota ', 'kab. ', 'kab ', 'sppg ']:
        if s.startswith(prefix):
            s = s[len(prefix):]
    return s

def merge_and_deduplicate(pdf_df: pd.DataFrame, starter_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge PDF extracted data with starter CSV, removing duplicates.
    Duplicate detection: same date + similar location text.
    Uses date + region + normalized location substring matching to catch
    true duplicates while preserving different incidents on the same date
    in the same province.
    """
    # Combine both dataframes (PDF first so it takes priority)
    combined = pd.concat([pdf_df, starter_df], ignore_index=True)
    
    # Sort by date
    combined = combined.sort_values('date').reset_index(drop=True)
    
    # Create normalized location for dedup
    combined['_norm_loc'] = combined['location'].apply(_normalize_location)
    combined['_dedup_key'] = combined['date'].astype(str) + '|' + combined['region'] + '|' + combined['_norm_loc']
    
    # For rows with the same date+region, check if locations overlap
    # Group by date + region, then within each group check for substring matches
    result_indices = []
    seen_keys = set()
    
    for idx, row in combined.iterrows():
        date_str = str(row['date'].date()) if hasattr(row['date'], 'date') else str(row['date'])[:10]
        region = row['region']
        norm_loc = row['_norm_loc']
        
        # Check if this is a duplicate by looking for overlap with seen entries
        is_dup = False
        group_key = f"{date_str}|{region}"
        
        for seen_key in seen_keys:
            if seen_key.startswith(group_key + '|'):
                seen_loc = seen_key[len(group_key) + 1:]
                # Check for significant substring overlap (both directions)
                # Use the shorter location as the query
                short, long = (seen_loc, norm_loc) if len(seen_loc) < len(norm_loc) else (norm_loc, seen_loc)
                # Extract key location words (>3 chars) for matching
                short_words = {w for w in short.split() if len(w) > 3}
                long_words = {w for w in long.split() if len(w) > 3}
                if short_words and long_words:
                    overlap = short_words & long_words
                    if len(overlap) >= max(1, min(len(short_words), len(long_words)) // 2):
                        is_dup = True
                        break
        
        if not is_dup:
            result_indices.append(idx)
            seen_keys.add(f"{group_key}|{norm_loc}")
    
    dedup = combined.loc[result_indices].drop(columns=['_norm_loc', '_dedup_key'])
    
    return dedup.sort_values('date').reset_index(drop=True)

def filter_wilayah_ii(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for Wilayah II (Jawa) only"""
    return df[df['region'].isin(WILAYAH_II_PROVINCES.values())].reset_index(drop=True)

def main():
    print("=" * 80)
    print("NUTRIWATCH: Extract Incidents from Wikipedia PDF")
    print("=" * 80)
    
    # Extract from PDF
    print("\n[1] Extracting incidents from PDF Wikipedia...")
    pdf_df = create_incidents_dataframe()
    print(f"    ✓ Extracted {len(pdf_df)} records from PDF")
    print(f"    ✓ Provinces: {pdf_df['region'].nunique()} unique")
    print(f"    ✓ Date range: {pdf_df['date'].min().date()} to {pdf_df['date'].max().date()}")
    
    # Load starter CSV
    print("\n[2] Loading incident_records_starter.csv...")
    starter_df = load_starter_csv()
    print(f"    ✓ Loaded {len(starter_df)} records")
    
    # Merge and deduplicate
    print("\n[3] Merging and deduplicating...")
    all_incidents = merge_and_deduplicate(pdf_df, starter_df)
    print(f"    ✓ Combined total: {len(all_incidents)} records after dedup")
    
    # Filter for Wilayah II (Jawa)
    print("\n[4] Filtering for Wilayah II (Jawa)...")
    wilayah_ii = filter_wilayah_ii(all_incidents)
    print(f"    ✓ Wilayah II total: {len(wilayah_ii)} records")
    print(f"    ✓ Provinces in Wilayah II: {sorted(wilayah_ii['region'].unique())}")
    
    # Save all incidents
    all_incidents.to_csv('incidents_full.csv', index=False, date_format='%Y-%m-%d')
    print(f"\n[5] Saved all incidents to: incidents_full.csv")
    
    # Save Wilayah II only
    wilayah_ii.to_csv('incidents_wilayah_ii.csv', index=False, date_format='%Y-%m-%d')
    print(f"[6] Saved Wilayah II incidents to: incidents_wilayah_ii.csv")
    
    # Statistics
    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80)
    print(f"\nTotal incidents (all regions): {len(all_incidents)}")
    print(f"Wilayah II (Jawa) incidents: {len(wilayah_ii)}")
    print(f"Percentage Wilayah II: {len(wilayah_ii)/len(all_incidents)*100:.1f}%")
    
    print(f"\nBreakdown by Wilayah II province:")
    wilayah_ii_counts = wilayah_ii['region'].value_counts()
    for province, count in wilayah_ii_counts.items():
        print(f"  - {province}: {count} incidents")
    
    print(f"\nDate range:")
    print(f"  - Earliest: {all_incidents['date'].min().date()}")
    print(f"  - Latest: {all_incidents['date'].max().date()}")
    print(f"  - Span: {(all_incidents['date'].max() - all_incidents['date'].min()).days} days")
    
    print(f"\nTotal victims (Wilayah II): {wilayah_ii['victim_count'].sum()}")
    print(f"Average victims per incident (Wilayah II): {wilayah_ii['victim_count'].mean():.0f}")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    main()

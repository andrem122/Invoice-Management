#!/bin/bash
cd /home/genuwine12/Tasks
source virtualenvwrapper.sh
workon Invoice-Management-virtualenv

# Contact Leads

# Mayfair At Lawnwood
python contact_leads.py -a '1800 Nebraska Ave, Fort Pierce, FL 34950' -n 'Mayfair At Lawnwood' -p '(772) 242-3154' -pid '1' -notify 'contact@mayfairatlawnwood.com' -e 'alan@graystonerealtyfl.com' 'contact@mayfairatlawnwood.com' 'andre@graystonerealtyfl.com' -epass '@10697Rambo' 'Gs({.MTRd^60' '537H%[*tsnap]Ty' -eserver 'mail.graystonerealtyfl.com' 'mail.mayfairatlawnwood.com' 'mail.graystonerealtyfl.com' -l 'https://forms.gle/e9fJKCU3UxF6VLsq7' -emailbrands 'zillow' 'apartments' 'move'

# Hidden Villas
# python contact_leads.py -a '2929 Panthersville Rd, Decatur, GA 30034' -n 'Hidden Villas Apartments' -p '(786) 818-3015' -pid '2' -notify 'andre.mashraghi@gmail.com' 'rene@bluedrg.com' 'sabrina@bluedrg.com' -e 'hiddenvillasapartments@gmail.com' -epass 'Hiddenvillas' -eserver 'imap.gmail.com' -l 'https://forms.gle/PP5ndxtFpAi2hek7A' -emailbrands 'apartments'

# 312 Northwood
# python contact_leads.py -a '312 23rd St, West Palm Beach, FL 33407' -n '312 Northwood Apartments' -p '(561) 629-3941' -pid '3' -notify 'andre.mashraghi@gmail.com' '312northwoodnotify@novaonesoftware.com' -e '312northwoodleads@novaonesoftware.com' -epass ')z4VXp2A%O1s9' -eserver 'mail.privateemail.com' -l '' -emailbrands 'apartments'

# Send appointment invite text to qualified leads

# Hidden Villas
# python send_text_to_qualified_leads.py -a '2929 Panthersville Rd, Decatur, GA 30034' -n 'Hidden Villas Apartments' -p '(786) 818-3015' -pid '2' -notify 'andre.mashraghi@gmail.com' -e 'andre.mashraghi@gmail.com' -epass 'fsznnxmjkivumdyo' -eserver 'imap.gmail.com' -l 'https://www.novaonesoftware.com/appointments/new?c=2'

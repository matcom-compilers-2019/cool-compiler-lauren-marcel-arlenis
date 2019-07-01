# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
# OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
# echo "The_Coolest v1.0"   # Recuerde cambiar estas
# echo "Copyright (c) 2019: Lauren, Marcel, Arlenis"    # líneas a los valores correctos

# Llamar al compilador
python3 ./main.py $INPUT_FILE
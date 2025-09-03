import json
import uuid
import re
def startManager():
  print(
    """=== GESTOR DE CLIENTES ===\n
    (1) Registrar nuevo cliente
    (2) Ver todos los clientes
    (3) Buscar cliente
    (4) Actualizar cliente
    (5) Borrar cliente
    (0) Salir\n"""
  )
  selectClient = str(input('Selecciona una opcion: '))
  
  match selectClient:
    case '1':
      addCustomer()
    
    case '2':
      showCustomers()
    
    case '3':
      searchCustomer()
      
    case '4':
      updateClient()

# Ask user for customer information and return it as a dictionary
def askForInfo(update = False, field = 0):
  print("=== REGISTRO DE USUARIO ===")
  
  def name_regex(name):
    """Valida que el nombre solo contenga letras y espacios"""
    return bool(re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{2,25}$', name))
  
  def lastName_regex(lastName):
    """Valida que el apellido solo contenga letras y espacios"""
    return bool(re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{2,40}$', lastName))

  def phoneNumber_regex(phoneNumber):
    """Valida números de teléfono con diferentes formatos"""
    return bool(re.match(r'^(\+?\d{1,3}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$', phoneNumber))

  def email_regex(email):
    """Valida formato de email"""
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
  
  def validateData(message, validationFunction, errorMessage):
    """Función helper para obtener datos válidos"""
    while True:
      dato = input(message).strip()
      if validationFunction(dato):
        return dato
      else:
        print(errorMessage)
  
  def validateName():
    name = validateData(
      'Introduzca nombre/s: ',
      name_regex,
      "❌ Error: El nombre debe contener solo letras y tener entre 2-25 caracteres"
    )
    return name
  
  def validateLastName():
    lastName = validateData(
      'Introduzca apellidos: ',
      lastName_regex,
      "❌ Error: Los apellidos deben contener solo letras y tener entre 2-40 caracteres"
    )
    return lastName

  def validatePhoneNumber():
    phoneNumber = validateData(
      'Introduzca el número telefónico: ',
      phoneNumber_regex,
      "❌ Error: Formato de teléfono inválido. Ejemplos: 1234567890, +1-234-567-8901"
    )
    return phoneNumber
  
  def validateEmail():
    email = validateData(
      'Introduzca un correo electrónico: ',
      email_regex,
      "❌ Error: Formato de email inválido. Ejemplo: usuario@dominio.com"
    )
    return email
  
  if update and field:
    match field:
      case 1:
        return validateName()
      case 2:
        return validateLastName()
      case 3:
        return validatePhoneNumber()
      case 4:
        return validateEmail()
      case 5:
        return 'jolines'
      
  else:
    return {
      'id': str(uuid.uuid4()),
      'name': validateName(),
      'lastName': validateLastName(),
      'phoneNumber': validatePhoneNumber(),
      'email': validateEmail()
    }

"""
Loads customers from customer.json file.
Args:
  errorMessage (str): The message to be displayed if the file is not found.
  createRegister (bool): If True and the file is not found, a new empty register is created.
Returns:
  dict: The loaded customers, or an empty dictionary if the file is not found and createRegister is True.
"""
def loadCustomers(errorMessage = 'File not found', createRegister = False):
  try:
      with open('customer.json', 'r') as data:
        customers = json.load(data)
  except FileNotFoundError:
    if createRegister:
      print('El archivo no existe, se creara un nuevo registro')
      customers = []
    else:
      print(errorMessage)
  
  return customers

"""
Adds a new customer to the customer.json file.
If the file doesn't exist, a new empty register is created.
The user is prompted to enter the customer's information.

Raises:
  Exception: If the file can't be accessed or written.
"""
def addCustomer():
  try:
    customers = loadCustomers(createRegister=True)
      
    # add a new customer
    newCustomer = askForInfo()
    customers.append(newCustomer)
    
    with open('customer.json', 'w') as data:
      json.dump(customers, data, indent=2, ensure_ascii=False)
      
    print('Cliente agregado satisfactoriamente')
        
  except Exception as e:
    print(f'Ha ocurrido un error: {e}')


"""
Shows all customers from the customer.json file.

If the file doesn't exist, an error message is displayed.

Raises:
  Exception: If the file can't be accessed or written.
"""
def showCustomers():
  try:
    customers = loadCustomers()
      
    print("LISTA DE CLIENTES: \n")
    for client in customers:
      print(f"CLIENTE:\nID: {client['id']}\nNombre: {client["name"]}\nApellidos: {client["lastName"]}\nNumero telefonico: {client["phoneNumber"]}\nEmail: {client["email"]}\n")
    
  except Exception as e:
    print(f'Ha ocurrido un error: {e}')

    
def searchCustomer():
  """
  Search for a customer in the customer.json file.
  
  The user is prompted to enter some data to search for the customer.
  If the data is found in any field of a customer, the customer is printed.
  
  If the file is not found, an error message is displayed.
  
  Raises:
    Exception: If the file can't be accessed or written.
  """
  try:
    customers = loadCustomers()
    
    if customers:
      coincidences = 0
      data = input('Introduce algun dato de la persona que deseas buscar: ').lower().strip()
      for client in customers:
        for key in client.keys():
          if data in client[key].lower():
            coincidences += 1
            print(f"CLIENTE:\nID: {client['id']}\nNombre: {client["name"]}\nApellidos: {client["lastName"]}\nNumero telefonico: {client["phoneNumber"]}\nEmail: {client["email"]}\n")
      print(f'\nSe ha hallado {coincidences} coincidencias.\n')
          

  except Exception as e:
    print(f'Ha ocurrido un error: {e}')

def saveCustomers(customers):
  """Guarda la lista de clientes en el archivo JSON"""
  try:
    with open('clientes.json', 'w', encoding='utf-8') as archivo:
      json.dump(customers, archivo, indent=2, ensure_ascii=False)
    return True
  except Exception as e:
    print(f"Error al guardar: {e}")
    return False

def updateClient():
  try: 
    customers = loadCustomers()
    if not customers:
      print("No hay clientes registrados.")
      return
    
    # search customers
    options = []
    data = input('Introduce algun dato de la persona que deseas buscar para actualizar: ').lower().strip()
    
    for client in customers:        
      for key in client:
        if data in str(client[key]).lower():
          options.append(client)
          print(f'\nCLIENTE:\nID: {client["id"]}\nNumero: {len(options)}\nNombre: {client["name"]}\nApellido: {client["lastName"]}\nNumero telefonico: {client["phoneNumber"]}\nEmail: {client["email"]}\n')
          break
    
    if not options:
      print("No se han encontrado coincidencias de clientes para modificar con los datos que ingresaste")
      return
    
    # helper function to show options
    def mostrar_opciones():
      print(f"\n{'='*50}")
      print(f"Se encontraron {len(options)} cliente(s):")
      for i, client in enumerate(options, 1):
        print(f"{i}. {client['name']} {client['lastName']} - {client['email']}")
      print(f"{'='*50}")
    
    while True:
      mostrar_opciones()
      selectClient = input('Ingrese el número del cliente a modificar o "salir" para finalizar: ').lower().strip()
      
      if selectClient == "salir":
        return
      
      if not selectClient.isdigit():
        print("❌ Error: Debe ingresar un número")
        continue
      
      selectClient_int = int(selectClient)
      if selectClient_int < 1 or selectClient_int > len(options):
        print(f"❌ Error: Debe ingresar un número entre 1 and {len(options)}")
        continue
      
      cliente_seleccionado = options[selectClient_int - 1]
      break
    
    while True:
      print(f"\nModificando cliente: {cliente_seleccionado['name']} {cliente_seleccionado['lastName']}")
      print("1. Modificar nombre")
      print("2. Modificar apellido")
      print("3. Modificar número telefónico")
      print("4. Modificar email")
      print("5. Salir")
      
      selectOption = input('Seleccione una opción: ').strip()
      
      if selectOption == "5":
        print("Modificación cancelada.")
        return
      
      if not selectOption.isdigit() or int(selectOption) not in range(1, 5):
        print("❌ Opción inválida")
        continue
      
      selectOption_int = int(selectOption)
      campo_anterior = None
      campo_nuevo = None
      
      # modify selected field
      match selectOption_int:
        case 1:
          campo_anterior = cliente_seleccionado['name']
          campo_nuevo = input("Nuevo nombre: ").strip()
          cliente_seleccionado['name'] = campo_nuevo
        case 2:
          campo_anterior = cliente_seleccionado['lastName']
          campo_nuevo = input("Nuevo apellido: ").strip()
          cliente_seleccionado['lastName'] = campo_nuevo
        case 3:
          campo_anterior = cliente_seleccionado['phoneNumber']
          campo_nuevo = input("Nuevo número telefónico: ").strip()
          cliente_seleccionado['phoneNumber'] = campo_nuevo
        case 4:
          campo_anterior = cliente_seleccionado['email']
          campo_nuevo = input("Nuevo email: ").strip()
          cliente_seleccionado['email'] = campo_nuevo
      
      # confirm changes
      print(f"\nCampo modificado:")
      print(f"Anterior: {campo_anterior}")
      print(f"Nuevo: {campo_nuevo}")
      
      confirmar = input("\n¿Guardar cambios? (s/n): ").lower().strip()
      if confirmar == 's':
        # update in the main list
        for i, client in enumerate(customers):
          if client['id'] == cliente_seleccionado['id']:
            customers[i] = cliente_seleccionado
            break
          
        # save on the archive
        if saveCustomers(customers):
          print("✅ Usuario modificado exitosamente")
        else:
          print("❌ Error al guardar los cambios")
        
        break
      else:
        print("❌ Cambios descartados")
        # reverse changes
        match selectOption_int:
          case 1: cliente_seleccionado['name'] = campo_anterior
          case 2: cliente_seleccionado['lastName'] = campo_anterior
          case 3: cliente_seleccionado['phoneNumber'] = campo_anterior
          case 4: cliente_seleccionado['email'] = campo_anterior
        break

  except Exception as e:
    print(f'❌ Ha ocurrido un error: {e}')
        
def deleteClient():
  try: 
    customers = loadCustomers()
    if not customers:
      print("No hay clientes registrados en el sistema.")
      return
    
    options = []
    data = input('Introduce algún dato del cliente que deseas eliminar: ').lower().strip()
    
    # look for matching customers
    for client in customers:
      for key in client.keys():
        if data in str(client[key]).lower():
          options.append(client)
          print(f"""\nCLIENTE ENCONTRADO:
Nombre: {client["name"]}
Apellido: {client["lastName"]}
Número telefónico: {client["phoneNumber"]}
Email: {client["email"]}
ID: {client["id"]}
""")
          break
    
    if not options:
      print("No se encontraron clientes que coincidan con la búsqueda.")
      return
    
    # assign numbers for selections
    for i, client in enumerate(options, 1):
      client["selection_number"] = i
    
    # show results with numbers
    print("\n" + "="*50)
    print("CLIENTES ENCONTRADOS:")
    for client in options:
      print(f"""[{client['selection_number']}] {client['name']} {client['lastName']}
   Teléfono: {client['phoneNumber']}
   Email: {client['email']}
   ID: {client['id']}
""")
    
    # validate selection
    while True:
      try:
        selection = input(f'Se encontraron {len(options)} cliente(s). Ingrese el número del cliente a eliminar (0 para cancelar): ')
        
        if selection == '0':
          print("Operación cancelada.")
          return
        
        selection_num = int(selection)
        if 1 <= selection_num <= len(options):
          selected_client = options[selection_num - 1]
          break
        else:
          print(f"Por favor, ingrese un número entre 1 y {len(options)} o 0 para cancelar.")
          
      except ValueError:
        print("Por favor, ingrese un número válido.")
    
    # confirm delete
    print(f"\n⚠️  CLIENTE SELECCIONADO PARA ELIMINAR:")
    print(f"Nombre: {selected_client['name']} {selected_client['lastName']}")
    print(f"Teléfono: {selected_client['phoneNumber']}")
    print(f"Email: {selected_client['email']}")
    print(f"ID: {selected_client['id']}")
    
    confirmacion = input("\n¿Está seguro de que desea eliminar este cliente? (sí/no): ").lower().strip()
    
    if confirmacion in ['sí', 'si', 's', 'yes', 'y']:
      # delete client of main list
      for i, client in enumerate(customers):
        if client['id'] == selected_client['id']:
          deleted_client = customers.pop(i)
          break
      
      # save changes
      if saveCustomers(customers):
        print(f"✅ Cliente {deleted_client['name']} {deleted_client['lastName']} eliminado exitosamente.")
      else:
        print("❌ Error al guardar los cambios.")
    else:
      print("Operación cancelada.")
  
  except Exception as e:
    print(f'❌ Ha ocurrido un error inesperado: {e}')

startManager()

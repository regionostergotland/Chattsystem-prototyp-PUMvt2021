# PUM2
Kandidatprojekt

Bakgrund:

Ett chattsystem har utvecklats för kunden Region Östergötland. Chattsystemet är en prototyp för att testa olika alternativ och ideer för ett eventuellt framtida chattsystem mellan patienter och vårdpersonal. Systemet fokuserar på förgrening av konversationer, markering av viktig text av vårdpersonal och patient-vårdpersonal interaktioner. Systemet har dessutom en enkel chattbott. 

Chattsystemet är utvecklat av grupp 2 i kandidatprojektkursen TDDD96 vid Linköpings universitet under våren 2021. 


Hur körs systemet?

Innan man kan köra run.bat för att starta servern på sin egen dator måste programmeringsspråket Python vara installerat. När du har installerat Python ska du dubbelklicka på run.bat. Filen kommer att installera alla nödvändiga bibliotek som krävs för att ha ett fungerande Chattsystem. 
När run.bat är färdig är servern igång och systemet går att användas på egna dator. För att komma åt patientsidan av applikationen skriver man in i följande länk i sin webbläsare: “http://localhost:5000/chat”. För att komma åt personalsidan av applikationen så skriver man in följande länk i sin webbläsare: “http://localhost:5000/chatpersonal”.


När man är inne i systemet:

Det finns två typer av användare, patienter och personal. Patienten kan se alla chatter patienten är en del av, patienten kan byta mellan dessa chatter genom att klicka på ikonerna i högra hörnet. Om chatten patienten kollar på är förgrenad från en annan chatt kan patienten återvända till föräldrachatten genom att klicka på chattens namn i övre delen av skärmen. Personalanvändare kan göra allt det patienten kan ovan men kan utöver det även skapa och stänga chatter, bjuda in användare till chatter samt markera text i chatterna. Som patient kan man även “identifiera” sig genom att klicka på knappen logga in och skriva in ett nummer från 1-4.  

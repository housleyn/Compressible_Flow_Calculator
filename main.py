from dynamicFlowCalculatorApp import DynamicFlowCalculatorApp

def main():
    try:
        app = DynamicFlowCalculatorApp()
        app.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")  # Keeps the window open to view errors

if __name__ == "__main__":
    main()

from djitellopy import Tello
import time
import sys

def main():
    print("🛰️ Initializing Tello and connecting over Wi-Fi...")
    
    try:
        drone = Tello()
    except OSError:
        print("\n❌ Error: UDP Port 8889 is already in use!")
        print("👉 Please close other Python terminals.")
        sys.exit(1)

    try:
        drone.connect()
    except Exception as conn_err:
        print(f"\n❌ Wi-Fi Connection Failed: {conn_err}")
        print("\n👉 Quick Checklist:")
        print("  1. Make sure Tello is powered on (LED blinking yellow fast).")
        print("  2. Verify PC Wi-Fi is connected to 'TELLO-AABFD8'.")
        print("  3. Make sure your phone isn't connected to the drone.")
        sys.exit(1)

    is_flying = False

    try:
        temp = drone.get_temperature()
        batt = drone.get_battery()
        print(f"\n✅ Connected successfully!")
        print(f"  🔋 Battery: {batt}%")
        print(f"  🌡️  Temp   : {temp} °C")

        # Temperature Safety Guard
        if temp >= 85:
            print("\n⚠️ Warning: Drone is too hot (>85°C). Please turn it off and let it cool down.")
            return

        # Battery Safety Guard
        if batt < 20:
            print("\n⚠️ Warning: Battery is below 20%. Please recharge before flying.")
            return

        print("\n🚀 Taking off...")
        drone.takeoff()
        is_flying = True

        print("⏱️ Hovering steadily for 5 seconds (self-cooling)...")
        time.sleep(5)

        print("🛬 Landing...")
        drone.land()
        is_flying = False
        print("✅ Flight test complete!")

    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user! Landing immediately...")
        if is_flying:
            drone.land()
            is_flying = False
    except Exception as e:
        print(f"\n❌ Flight error: {e}")
    finally:
        if is_flying:
            try:
                drone.land()
            except:
                pass
        drone.end()

if __name__ == "__main__":
    main()

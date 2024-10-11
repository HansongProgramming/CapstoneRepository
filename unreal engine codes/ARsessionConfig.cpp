UCLASS(){
    class AiCore_API AMyARpawn : public ADefaultPawn{
        GENERATED_BODY()

        public:
            UPROPERTY(EditAnywhere)
            UARSessionConfig* ARConfig;
            AMyARpawn();

        protected:
            virtual void BeginPlay() override;
    }
}

AMyARpawn::AMyARpawn(){
    ARConfig = CreateDefaultSubobject<UARSessionConfig>(TEXT("ARSessionConfig"));
}

void AMyARpawn::BeginPlay(){
    Super::BeginPlay();

    UARBlueprintLibrary::StartARSession(ARConfig);
}

void AMyARpawn::TraceMeasurePoint(){
    FVector2D ScreenLocation;
    FHitResult HitResult;
    if(UARBlueprintLibrary::LineTraceTrackedObjects(ScreenLocation, true, HitResult)){
        FVector2D HitLocation = HitResult.Location;
    }
}

float Distance = FVector::Dist(Point1,Point2);

void AMyARpawn::TakeScreenshot(){
    FScreenshotRequest::RequestScreenshot(FString(TEXT("Measurement.png")),false, false);
}

AMyARGameMode::AMyARGameMode(){
    DefaultPawnClass = AMyARpawn::StaticClass();
}
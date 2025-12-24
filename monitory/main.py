from modules.nodes.healthCheck import check_nodes
from modules.nodes.resources import get_node_resources
from modules.mail.sendmail import send_alert_email
from modules.utils.pdfgenerator import PDFReport
from datetime import datetime


def main():
    # Node  health check

    # PDF Header 
    pdf = PDFReport("/tmp/reporte_cluster.pdf")

    pdf.add_title("Kubernetes Cluster Monitoring Report")

    pdf.add_paragraph(
        "This report provides an overview of the cluster's health, "
        "covering nodes, pods, and services.."
    )

    # Check node conditions
    print("Monitoring Nodes...\n")
    node_rows, node_issues = check_nodes()
    pdf.add_section("NODE CONDITIONS")
    pdf.add_table(
        ["Node", "Condition", "Code", "Details"],
        node_rows
    )

    
    # Node resources usaged
    print("Monitoring Nodes resources...\n")
    resource_rows, resource_issues = get_node_resources()
    pdf.add_section("NODE RESOURCE USAGE")
    pdf.add_table(
        ["Node", "CPU", "CPU %", "Memory", "Mem %"],
        resource_rows
    )
    
    
    pdf.save()

    
    
    # Send email with report PDF
    print("Sending report...\n")
    date = datetime.now().strftime("%Y-%m-%d")
    message=(
            "Hi,\n\n"
            "Automated environment monitoring has been performed; the status summary is provided below:\n"
        )
    
    message += f"Nodes: {'NOK' if node_issues else 'OK'}\n"



    if node_issues or resource_issues:
        message+=(
            "Cluster errors were detected; the PDF report is attached below\n\n"
            "This monitoring was performed automatically; therefore, discrepancies may occur. "
            "We recommend a manual review by a technical specialist to confirm or dismiss the reported issues\n\n\n"
            "Best regards."
        )
        send_alert_email(f"Monitoring report DEV environment - {date}",message,"/tmp/reporte_cluster.pdf")
        print("Monitoring finished...\n")
        exit(1)
    else:
        message+=(
            "This email and monitoring report were automatically generated.\n\n"
            "Best regards."
        )
        send_alert_email(f"Monitoring report DEV environment - {date}",message,"/tmp/reporte_cluster.pdf")
        print("Monitoring finished...\n")
        exit(0)
    

if __name__ == "__main__":
    main()

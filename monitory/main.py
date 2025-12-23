from modules.nodes.healthCheck import check_nodes
from modules.nodes.resources import get_node_resources
from modules.pods.healthCheck import check_pod_health
from modules.services.healthCheckTCP import get_services_health
from modules.utils.utils import print_table
from modules.mail.sendmail import send_alert_email
from modules.utils.pdfreport import generate_pdf_report
from modules.utils.pdfgenerator import PDFReport
from modules.storage.nfsfilesystem import get_nfs_filesystem_usage
from modules.storage.getstorageusage import get_nfs_usage_by_pv
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
    
    # Check pv usaged
    print("Monitoring Persisten Volume used...\n")
    nfs_rows, nfs_issues = get_nfs_usage_by_pv("/mnt/nfs-server/")
    pdf.add_section("PERSISTEN VOLUME USED")
    pdf.add_table(
        ["PV", "folder","Used", "Size", "Used %", "Estatus"],
        nfs_rows
    )
    
    # NFS Check
    print ("NFS Cheking ...\n")
    fs = get_nfs_filesystem_usage("/mnt/nfs-server/")
    pdf.add_section("NFS SERVER STATUS")
    pdf.add_table(
        ["FileSystem", "Size","Used", "Available", "Used %"],
        [[fs["filesystem"],fs["size"],fs["used"],fs["available"],fs["use_pct"]]]
    )

    # Health check Pods
    print("Monitoring pods health...\n")
    pod_rows, pod_issues = check_pod_health()
    
    pdf.add_section("PODS UNHEALTHY")
    pdf.add_table(
        ["Namespace", "Pod", "Status", "Error Code", "Details"],
        pod_rows
    )
    

    #Health check svc
    print("Monitoring service health...\n")
    svc_rows, svc_err = get_services_health()
    pdf.add_section("SERVICE HEALTH STATUS")
    pdf.add_table(
        ["Namespace", "Service", "Port", "Estatus", "Details"],
        svc_rows
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
    message += f"Pods: {'NOK' if pod_issues else 'OK'}\n"
    message += f"Services: {'NOK' if svc_err else 'OK'}\n"


    if node_issues or resource_issues or svc_err or pod_issues:
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
